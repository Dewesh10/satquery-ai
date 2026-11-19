import pytest
from app.core.config import settings
from app.services.planner import planner
from app.services.query_store import query_store
from app.services.anomaly_detector import anom_detector
from app.services.alert_dispatcher import alert_dispatcher
from app.services.health_monitor import health_monitor
from app.services.digest_generator import digest_generator
from app.services.raster import raster_engine
from app.services.eval_benchmarks import evaluate_sen1floods11_sar, evaluate_oscd_urban
from app.services.llm_planner import llm_query_planner, validate_plan_schema
from app.services.ml_flood_classifier import ml_flood_engine
from app.services.sentinel_monitor import sentinel_monitor
from app.services.geo_utils import calculate_geodesic_polygon_area, get_sentinel2_mgrs_info, compute_custom_aoi_zonal_stats
from app.services.hitl import hitl_service

# =====================================================================
# 1. Planner & Explicit Preset Preservation Tests
# =====================================================================
def test_planner_honors_explicit_preset():
    plan = planner.plan_query("Show built-up growth in Dubai", user_preset_id="dubai_urban")
    assert plan["selected_preset_id"] == "dubai_urban"
    assert "compiled_plan" in plan

def test_planner_named_location_resolution():
    plan = planner.plan_query("Analyze urban expansion in Dubai")
    assert plan["selected_preset_id"] == "dubai_urban"

def test_planner_structure():
    plan = planner.plan_query("deforestation in amazon")
    assert "dag_steps" in plan
    assert len(plan["dag_steps"]) > 0
    assert "intent" in plan

def test_llm_query_planner_schema_validation():
    plan = llm_query_planner.compile_prompt("Analyze flood inundation in Assam across 2023")
    assert validate_plan_schema(plan) is True
    assert plan["intent"] == "FLOOD_INUNDATION"
    assert plan["sensor_modality"] == "SAR_SENTINEL1"

# =====================================================================
# 2. Query Store & Replay Tests
# =====================================================================
def test_query_store_save_and_retrieve():
    run_id = "RUN-TEST-001"
    plan = {"query": "test query", "selected_preset_id": "dubai_urban"}
    analytics = {"area_sq_km": 12.5, "percentage_change": "+5.4%"}
    evidence = {"evidence_text": "Evidence verified."}
    
    saved = query_store.save_run(run_id, plan, analytics, evidence)
    assert saved["run_id"] == run_id
    
    fetched = query_store.get_run(run_id)
    assert fetched is not None
    assert fetched["run_id"] == run_id
    assert fetched["preset_id"] == "dubai_urban"
    assert fetched["analytics"]["area_sq_km"] == 12.5

def test_query_store_history():
    history = query_store.get_history(limit=5)
    assert isinstance(history, list)
    assert len(history) >= 1

def test_query_store_demo_snapshot():
    demo_runs = query_store.get_demo_snapshot()
    assert isinstance(demo_runs, list)
    assert len(demo_runs) == 5
    assert demo_runs[0]["preset_id"] == "dubai_urban"

# =====================================================================
# 3. Anomaly Detection & Webhook Dispatcher Tests
# =====================================================================
def test_anomaly_detector_observe_and_stats():
    for val in [10.0, 10.2, 9.8, 10.1, 9.9]:
        anom_detector.observe("sensor_test", {"area_delta": val})
    
    stats = anom_detector.get_stats()
    assert "sensor_test" in stats["presets_monitored"]
    assert stats["window_size"] == 10

def test_anomaly_detector_trigger_high_z_score():
    alerts = anom_detector.observe("sensor_test", {"area_delta": 999.0})
    assert isinstance(alerts, list)

def test_alert_dispatcher_registration():
    url = "https://discord.com/api/webhooks/test/123"
    alert_dispatcher.register(url)
    stats = alert_dispatcher.get_stats()
    assert stats["registered_webhooks"] >= 1
    assert url in stats["webhook_urls"]

# =====================================================================
# 4. Pipeline Health Monitor & AI Digest Tests
# =====================================================================
def test_pipeline_health_report():
    report = health_monitor.get_full_report(query_store, anom_detector, alert_dispatcher)
    assert "status" in report
    assert "database" in report
    assert "anomaly_detector" in report
    assert "components" in report

def test_digest_generation_and_caching():
    analytics = raster_engine.compute_change_analytics("dubai_urban")
    digest = digest_generator.generate("dubai_urban", analytics)
    assert "digest" in digest
    assert digest["preset_id"] == "dubai_urban"

# =====================================================================
# 5. Public Benchmark Evaluations (Sen1Floods11 & OSCD)
# =====================================================================
def test_sen1floods11_evaluation():
    bm = evaluate_sen1floods11_sar(threshold_db=-16.5)
    assert "metrics" in bm
    assert bm["metrics"]["iou_jaccard"] > 0.85
    assert bm["metrics"]["precision"] > 0.85
    assert bm["metrics"]["recall"] > 0.85

def test_oscd_urban_evaluation():
    bm = evaluate_oscd_urban(threshold_delta=0.22)
    assert "metrics" in bm
    assert bm["metrics"]["iou_jaccard"] > 0.65
    assert bm["metrics"]["f1_score"] > 0.75

# =====================================================================
# 6. Real ML Multi-Sensor Component vs Classical Method
# =====================================================================
def test_ml_model_evaluation():
    ml_eval = ml_flood_engine.get_evaluation()
    assert "RandomForestClassifier" in ml_eval["model_type"]
    assert ml_eval["ml_model_metrics"]["iou_jaccard"] >= ml_eval["classical_ndwi_baseline"]["iou_jaccard"]

# =====================================================================
# 7. End-to-End Closed Loop Alerting & HITL Feedback
# =====================================================================
def test_sentinel_closed_loop_flow():
    loop_res = sentinel_monitor.process_live_pass_and_evaluate_alert("AOI-WATCH-01", alert_dispatcher, query_store)
    assert loop_res["status"] == "CLOSED_LOOP_EVALUATION_COMPLETE"
    assert "threshold_breached" in loop_res

def test_hitl_feedback_and_tuning():
    fb = hitl_service.submit_correction("CHIP-99", "FALSE_POSITIVE", "Cloud reflection mistaken for water")
    assert fb["feedback_type"] == "FALSE_POSITIVE"
    tuning = hitl_service.get_active_threshold_tuning_recommendation()
    assert "recommended_threshold_adjustment" in tuning

# =====================================================================
# 8. Geodesic Shoelace & MGRS Tile Calculator Tests
# =====================================================================
def test_geodesic_shoelace_area():
    coords = [[25.0, 55.0], [25.0, 55.1], [25.1, 55.1], [25.1, 55.0]]
    res = calculate_geodesic_polygon_area(coords)
    assert res["area_sq_km"] > 100.0
    assert res["hectares"] > 10000.0

def test_mgrs_tile_locator():
    mgrs = get_sentinel2_mgrs_info(25.08, 55.12)
    assert mgrs["utm_zone"] == 40
    assert "s3://sentinel-cogs" in mgrs["aws_s3_prefix"]

def test_zonal_stats():
    coords = [[25.08, 55.12], [25.08, 55.25], [25.18, 55.25], [25.18, 55.12]]
    z_stats = compute_custom_aoi_zonal_stats(coords)
    assert z_stats["status"] == "ZONAL_STATS_COMPUTED"
    assert "mean_ndvi" in z_stats["spectral_indices"]
