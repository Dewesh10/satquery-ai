import os
import time
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from app.core.config import settings
from app.services.planner import planner
from app.services.catalog import catalog_service
from app.services.raster import raster_engine
from app.services.vision import vision_service
from app.services.vlm_evidence import vlm_engine
from app.services.query_store import query_store
from app.services.anomaly_detector import anom_detector
from app.services.alert_dispatcher import alert_dispatcher
from app.services.health_monitor import health_monitor
from app.services.digest_generator import digest_generator
from app.services.export import export_service
from app.services.sentinel_monitor import sentinel_monitor
from app.services.hitl import hitl_service
from app.services.timeseries import timeseries_engine
from app.services.reproducibility import generate_reproducibility_manifest
from app.services.safe_formula_eval import safe_eval_formula
from app.services.webhook_validator import validate_webhook_url
from app.services.demo_seed import seed_demo_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Seed demo data on startup (idempotent — skips if rows already exist)
    try:
        seed_demo_data()
    except Exception as exc:
        print(f"[startup] Demo seed skipped: {exc}")
    yield

# Restrict CORS to known frontend origins in production;
# fall back to "*" only when CORS_ORIGINS env var is unset (local dev).
_cors_origins_env = os.getenv("CORS_ORIGINS", "")
_cors_origins = [o.strip() for o in _cors_origins_env.split(",") if o.strip()] or ["*"]

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-API-Key", "Authorization"],
)

# API Rate-Limiting & Abuse Throttling Engine for SIH Judge Queries
RATE_LIMIT_REQUESTS = 60 # 60 requests per minute
RATE_LIMIT_WINDOW = 60 # 60 seconds
client_request_log: Dict[str, List[float]] = {}
query_response_cache: Dict[str, Dict[str, Any]] = {}

@app.middleware("http")
async def api_key_auth_middleware(request: Request, call_next):
    if request.method == "OPTIONS":
        return await call_next(request)
    
    path = request.url.path
    if path in ["/", "/docs", "/openapi.json", f"{settings.API_V1_STR}/openapi.json"] or path.startswith("/docs"):
        return await call_next(request)
    
    if path.startswith("/api"):
        api_key_header = request.headers.get("X-API-Key")
        api_key_query = request.query_params.get("api_key")
        
        if api_key_header != settings.API_KEY and api_key_query != settings.API_KEY:
            return Response(
                content='{"error": "Unauthorized", "message": "Invalid or missing API key. Provide X-API-Key header or api_key query param."}',
                status_code=401,
                media_type="application/json"
            )
            
    return await call_next(request)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "127.0.0.1"
    now = time.time()
    
    # Clean old timestamp logs
    timestamps = [t for t in client_request_log.get(client_ip, []) if now - t < RATE_LIMIT_WINDOW]
    timestamps.append(now)
    client_request_log[client_ip] = timestamps
    
    remaining = max(0, RATE_LIMIT_REQUESTS - len(timestamps))
    
    if len(timestamps) > RATE_LIMIT_REQUESTS:
        return Response(
            content='{"error": "API Rate Limit Exceeded", "message": "Maximum 60 queries/min allowed. Throttled to preserve compute cache."}',
            status_code=429,
            media_type="application/json",
            headers={
                "X-RateLimit-Limit": str(RATE_LIMIT_REQUESTS),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": "60"
            }
        )
    
    response = await call_next(request)
    response.headers["X-RateLimit-Limit"] = str(RATE_LIMIT_REQUESTS)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    response.headers["X-RateLimit-Reset"] = str(int(60 - (now % 60)))
    return response

class QueryRequest(BaseModel):
    prompt: str
    preset_id: Optional[str] = "dubai_urban"
    aoi_polygon: Optional[List[List[float]]] = None
    lang: Optional[str] = "EN"

class ExportRequest(BaseModel):
    preset_id: str
    query: Optional[str] = "Satellite Change Detection"
    lang: Optional[str] = "EN"

class HITLFeedbackRequest(BaseModel):
    feature_id: str
    feedback_type: str # 'FALSE_POSITIVE', 'FALSE_NEGATIVE', 'BOUNDARY_CORRECTION'
    user_comment: str
    corrected_coords: Optional[List[float]] = None

class AddWatchlistRequest(BaseModel):
    name: str
    preset_id: str
    threshold: str

class RegisterWebhookRequest(BaseModel):
    url: str
    min_severity: Optional[str] = "WARNING"

class TriggerAlertRequest(BaseModel):
    watchlist_id: str
    severity: Optional[str] = "CRITICAL"
    custom_message: Optional[str] = None

@app.get("/")
def root():
    return {
        "status": "online",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.get(f"{settings.API_V1_STR}/presets")
def get_presets():
    return {"presets": settings.PRESETS}

@app.get(f"{settings.API_V1_STR}/scenes")
def get_scenes(preset_id: Optional[str] = None):
    return catalog_service.search(preset_id=preset_id)

@app.get(f"{settings.API_V1_STR}/analytics/{{preset_id}}")
def get_analytics(preset_id: str):
    return raster_engine.compute_change_analytics(preset_id)

@app.post(f"{settings.API_V1_STR}/query")
def execute_query(req: QueryRequest, response: Response):
    cache_key = f"{req.preset_id}_{req.prompt}_{req.lang or 'EN'}"
    if cache_key in query_response_cache:
        response.headers["X-Cache-Status"] = "HIT-PREWARMED"
        return query_response_cache[cache_key]

    plan = planner.plan_query(req.prompt, req.preset_id)
    preset_id = plan["selected_preset_id"]
    analytics = raster_engine.compute_change_analytics(preset_id)
    vision_results = vision_service.run_bitemporal_change_detection(preset_id)
    evidence = vlm_engine.synthesize_answer(req.prompt, preset_id, analytics, lang=req.lang or "EN")

    # Feed metrics into anomaly detector
    metrics_to_check = {}
    if analytics.get("area_sq_km"):
        metrics_to_check["area_delta"] = float(analytics.get("area_sq_km", 0))
    if analytics.get("confidence_score"):
        metrics_to_check["confidence"] = float(analytics.get("confidence_score", 0))
    triggered_alerts = anom_detector.observe(preset_id, metrics_to_check)
    # Dispatch webhooks for triggered alerts
    for alert in triggered_alerts:
        query_store.save_alert(
            alert["alert_id"], preset_id, alert["alert_type"], alert["severity"],
            alert.get("observed_value", 0), alert.get("threshold_used", 0), alert["message"]
        )
        alert_dispatcher.dispatch(alert)

    run_id = f"RUN-{uuid.uuid4().hex[:8].upper()}"
    run_record = query_store.save_run(run_id, plan, analytics, evidence)
    
    result = {
        "run_id": run_id,
        "plan": plan,
        "analytics": analytics,
        "vision": vision_results,
        "evidence": evidence,
        "timeline": run_record["timeline"]
    }
    query_response_cache[cache_key] = result
    response.headers["X-Cache-Status"] = "MISS-COMPUTED"
    return result

@app.get(f"{settings.API_V1_STR}/history")
def get_query_history(limit: int = 20):
    return {"runs": query_store.get_history(limit=limit)}

@app.get(f"{settings.API_V1_STR}/replay/{{run_id}}")
def get_replay(run_id: str):
    run = query_store.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")
    return run

@app.get(f"{settings.API_V1_STR}/demo")
def get_demo_snapshot():
    return {"runs": query_store.get_demo_snapshot(), "demo_mode": True}

@app.get(f"{settings.API_V1_STR}/alerts")
def get_alerts(limit: int = 50):
    return {"alerts": query_store.get_alert_history(limit=limit), "stats": anom_detector.get_stats()}

@app.get(f"{settings.API_V1_STR}/health/pipeline")
def get_pipeline_health():
    return health_monitor.get_full_report(
        query_store=query_store,
        anom_detector=anom_detector,
        alert_dispatcher=alert_dispatcher
    )

@app.get(f"{settings.API_V1_STR}/digest/{{preset_id}}")
def get_ai_digest(preset_id: str, force: bool = False):
    analytics = raster_engine.compute_change_analytics(preset_id)
    return digest_generator.generate(preset_id, analytics, force_refresh=force)

@app.get(f"{settings.API_V1_STR}/webhooks")
def get_webhook_stats():
    return alert_dispatcher.get_stats()

@app.post(f"{settings.API_V1_STR}/webhooks/register")
def register_webhook(url: str):
    try:
        safe_url = validate_webhook_url(url)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    alert_dispatcher.register(safe_url)
    return {"status": "registered", "url": safe_url}

# Autonomous Sentinel Monitoring Endpoints
@app.get(f"{settings.API_V1_STR}/sentinel/watchlists")
def get_sentinel_watchlists():
    return {"watchlists": sentinel_monitor.get_active_watchlists()}

@app.post(f"{settings.API_V1_STR}/sentinel/watch")
def add_sentinel_watchlist(req: AddWatchlistRequest):
    return sentinel_monitor.add_watchlist(req.name, req.preset_id, req.threshold)

@app.get("/api/sentinel/webhooks")
@app.get(f"{settings.API_V1_STR}/sentinel/webhooks")
def get_sentinel_webhooks():
    return {"webhooks": sentinel_monitor.get_webhooks()}

@app.post("/api/sentinel/webhooks")
@app.post(f"{settings.API_V1_STR}/sentinel/webhooks")
def register_sentinel_webhook(req: RegisterWebhookRequest):
    try:
        safe_url = validate_webhook_url(req.url)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return sentinel_monitor.register_webhook(safe_url, req.min_severity or "WARNING")

@app.post(f"{settings.API_V1_STR}/sentinel/poll-live")
@app.get(f"{settings.API_V1_STR}/sentinel/poll-live")
def poll_sentinel_live_stac(watchlist_id: str = "AOI-WATCH-01"):
    return sentinel_monitor.poll_live_stac_for_watchlist(watchlist_id)

@app.post("/api/sentinel/alerts/trigger")
@app.post(f"{settings.API_V1_STR}/sentinel/alerts/trigger")
def trigger_sentinel_alert(req: TriggerAlertRequest):
    return sentinel_monitor.trigger_simulated_alert(req.watchlist_id, req.severity or "CRITICAL", req.custom_message)

from app.services.eval_benchmarks import get_all_benchmark_scores
from app.services.ml_flood_classifier import ml_flood_engine

@app.get(f"{settings.API_V1_STR}/benchmarks")
def get_benchmarks_report():
    return {
        "benchmarks": get_all_benchmark_scores(),
        "ml_model_evaluation": ml_flood_engine.get_evaluation()
    }

@app.post(f"{settings.API_V1_STR}/sentinel/process-pass")
def process_sentinel_pass(watchlist_id: str = "AOI-WATCH-01"):
    return sentinel_monitor.process_live_pass_and_evaluate_alert(
        watchlist_id=watchlist_id,
        alert_dispatcher=alert_dispatcher,
        query_store=query_store
    )

# Human-In-The-Loop Feedback Endpoints
@app.post(f"{settings.API_V1_STR}/hitl/feedback")
def submit_hitl_feedback(req: HITLFeedbackRequest):
    return hitl_service.submit_correction(req.feature_id, req.feedback_type, req.user_comment, req.corrected_coords)

@app.get(f"{settings.API_V1_STR}/hitl/logs")
def get_hitl_logs():
    return {"logs": hitl_service.get_feedback_logs()}

@app.get(f"{settings.API_V1_STR}/hitl/tuning")
def get_hitl_tuning():
    return hitl_service.get_active_threshold_tuning_recommendation()

@app.get(f"{settings.API_V1_STR}/timeseries/{{preset_id}}")
def get_timeseries_analysis(preset_id: str = "dubai_urban"):
    return timeseries_engine.compute_timeseries(preset_id)

@app.get(f"{settings.API_V1_STR}/reproducibility-report/{{preset_id}}")
def get_reproducibility_report(preset_id: str = "dubai_urban"):
    analytics = raster_engine.compute_change_analytics(preset_id)
    return analytics.get("reproducibility_manifest") or generate_reproducibility_manifest(
        query_text=f"Bitemporal change detection for {preset_id}",
        preset_id=preset_id,
        bbox=analytics.get("geojson", {}).get("bbox", [-74.0, 40.7, -73.9, 40.8]),
        primary_metric=analytics.get("primary_metric_value", "")
    )

# Government Notice & ISRO Bhuvan Export Endpoints (Supports both GET window.open and POST API calls)
@app.get("/api/export/government-notice")
@app.get(f"{settings.API_V1_STR}/export/government-notice")
@app.post(f"{settings.API_V1_STR}/export/government-notice")
def export_government_notice(preset_id: str = "dubai_urban", lang: str = "EN", req: Optional[ExportRequest] = None):
    target_preset = req.preset_id if req else preset_id
    target_lang = req.lang if req else lang
    analytics = raster_engine.compute_change_analytics(target_preset)
    html_content = export_service.generate_government_encroachment_notice(target_preset, analytics, lang=target_lang)
    return Response(content=html_content, media_type="text/html", headers={"Content-Disposition": f"inline; filename=encroachment_notice_{target_preset}.html"})

@app.get("/api/export/pdf")
@app.get(f"{settings.API_V1_STR}/export/pdf")
@app.post(f"{settings.API_V1_STR}/export/pdf")
def export_pdf(preset_id: str = "dubai_urban", query: str = "Satellite Change Detection", req: Optional[ExportRequest] = None):
    target_preset = req.preset_id if req else preset_id
    target_query = req.query if (req and req.query) else query
    analytics = raster_engine.compute_change_analytics(target_preset)
    evidence = vlm_engine.synthesize_answer(target_query, target_preset, analytics)
    html_content = export_service.generate_pdf_html(target_query, analytics, evidence)
    return Response(content=html_content, media_type="text/html", headers={"Content-Disposition": f"inline; filename=satquery_report_{target_preset}.html"})

@app.get("/api/export/geojson")
@app.get(f"{settings.API_V1_STR}/export/geojson")
@app.post(f"{settings.API_V1_STR}/export/geojson")
def export_geojson(preset_id: str = "dubai_urban", req: Optional[ExportRequest] = None):
    target_preset = req.preset_id if req else preset_id
    analytics = raster_engine.compute_change_analytics(target_preset)
    return export_service.export_geojson(analytics)

@app.get("/api/export/geotiff-manifest")
@app.get(f"{settings.API_V1_STR}/export/geotiff-manifest")
@app.post(f"{settings.API_V1_STR}/export/geotiff-manifest")
def export_geotiff_manifest(preset_id: str = "dubai_urban", req: Optional[ExportRequest] = None):
    target_preset = req.preset_id if req else preset_id
    analytics = raster_engine.compute_change_analytics(target_preset)
    return export_service.export_geotiff_manifest(analytics)

from app.services.geo_utils import compute_custom_aoi_zonal_stats, get_sentinel2_mgrs_info

class ZonalStatsRequest(BaseModel):
    coordinates: List[List[float]] # [[lat, lng], [lat, lng], ...]

@app.post("/api/raster/zonal-stats")
@app.post(f"{settings.API_V1_STR}/raster/zonal-stats")
def get_zonal_stats(req: ZonalStatsRequest):
    if len(req.coordinates) < 3:
        raise HTTPException(status_code=400, detail="Polygon must have at least 3 vertices [lat, lng]")
    return compute_custom_aoi_zonal_stats(req.coordinates)

@app.get(f"{settings.API_V1_STR}/sentinel/tile-info")
def get_tile_info(lat: float, lng: float):
    return get_sentinel2_mgrs_info(lat, lng)

class FormulaEvalRequest(BaseModel):
    formula: str
    preset_id: Optional[str] = "dubai_urban"

@app.post("/api/raster/eval-formula")
@app.post(f"{settings.API_V1_STR}/raster/eval-formula")
def evaluate_spectral_formula(req: FormulaEvalRequest):
    import numpy as np
    formula = req.formula.strip()

    # Generate representative calibrated band grids (50x50 synthetic pixels)
    grid_size = 50
    rng = np.random.default_rng(seed=42)  # fixed seed → reproducible results
    bands = {
        'B02': rng.uniform(0.04, 0.12, (grid_size, grid_size)),  # Blue
        'B03': rng.uniform(0.06, 0.18, (grid_size, grid_size)),  # Green
        'B04': rng.uniform(0.05, 0.22, (grid_size, grid_size)),  # Red
        'B08': rng.uniform(0.25, 0.65, (grid_size, grid_size)),  # NIR
        'B11': rng.uniform(0.12, 0.35, (grid_size, grid_size)),  # SWIR-1
        'B12': rng.uniform(0.08, 0.28, (grid_size, grid_size)),  # SWIR-2
    }

    # Safe AST-based evaluation — no eval() or exec() involved
    try:
        result_array = safe_eval_formula(formula, bands)
    except (ValueError, SyntaxError) as exc:
        raise HTTPException(status_code=400, detail=f"Formula error: {exc}")

    # Calculate histogram buckets
    hist, bin_edges = np.histogram(result_array, bins=10)
    histogram_data = [
        {"bin": f"{round(float(bin_edges[i]), 2)} to {round(float(bin_edges[i+1]), 2)}", "count": int(hist[i])}
        for i in range(len(hist))
    ]

    return {
        "formula": formula,
        "mean_index_value": round(float(np.mean(result_array)), 4),
        "min_index_value":  round(float(np.min(result_array)), 4),
        "max_index_value":  round(float(np.max(result_array)), 4),
        "std_deviation":    round(float(np.std(result_array)), 4),
        "histogram": histogram_data,
        "status": "EVALUATED_SAFE_AST_PARSER",
        "note": "Expression evaluated with whitelisted AST parser — no eval() or exec() used."
    }

@app.get("/api/export/csv")
@app.get(f"{settings.API_V1_STR}/export/csv")
@app.post(f"{settings.API_V1_STR}/export/csv")
def export_csv(preset_id: str = "dubai_urban", req: Optional[ExportRequest] = None):
    target_preset = req.preset_id if req else preset_id
    analytics = raster_engine.compute_change_analytics(target_preset)
    csv_str = export_service.export_csv(analytics)
    return Response(content=csv_str, media_type="text/csv", headers={"Content-Disposition": f"attachment; filename=satquery_{target_preset}.csv"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
