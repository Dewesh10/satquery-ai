import time
import uuid
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
from app.services.replay import replay_store
from app.services.export import export_service
from app.services.sentinel_monitor import sentinel_monitor
from app.services.hitl import hitl_service

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    
    run_id = f"RUN-{uuid.uuid4().hex[:8].upper()}"
    run_record = replay_store.save_run(run_id, plan, analytics, evidence)
    
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
    return sentinel_monitor.register_webhook(req.url, req.min_severity or "WARNING")

@app.post("/api/sentinel/alerts/trigger")
@app.post(f"{settings.API_V1_STR}/sentinel/alerts/trigger")
def trigger_sentinel_alert(req: TriggerAlertRequest):
    return sentinel_monitor.trigger_simulated_alert(req.watchlist_id, req.severity or "CRITICAL", req.custom_message)

# Human-In-The-Loop Feedback Endpoints
@app.post(f"{settings.API_V1_STR}/hitl/feedback")
def submit_hitl_feedback(req: HITLFeedbackRequest):
    return hitl_service.submit_correction(req.feature_id, req.feedback_type, req.user_comment, req.corrected_coords)

@app.get(f"{settings.API_V1_STR}/hitl/logs")
def get_hitl_logs():
    return {"logs": hitl_service.get_feedback_logs()}

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
