import pytest
from app.core.config import settings
from app.services.planner import planner
from app.services.query_store import query_store
from app.services.anomaly_detector import anom_detector
from app.services.alert_dispatcher import alert_dispatcher
from app.services.health_monitor import health_monitor
from app.services.digest_generator import digest_generator
from app.services.raster import raster_engine

# =====================================================================
# 1. Planner & Explicit Preset Preservation Tests
# =====================================================================
def test_planner_honors_explicit_preset():
    plan = planner.plan_query("Show built-up growth in Dubai", user_preset_id="dubai_urban")
    assert plan["selected_preset_id"] == "dubai_urban"

def test_planner_named_location_resolution():
    plan = planner.plan_query("Analyze urban expansion in Dubai")
    assert plan["selected_preset_id"] == "dubai_urban"

def test_planner_structure():
    plan = planner.plan_query("deforestation in amazon")
    assert "dag_steps" in plan
    assert len(plan["dag_steps"]) > 0
    assert "intent" in plan


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
    # Insert normal values
    for val in [10.0, 10.2, 9.8, 10.1, 9.9]:
        anom_detector.observe("sensor_test", {"area_delta": val})
    
    stats = anom_detector.get_stats()
    assert "sensor_test" in stats["presets_monitored"]
    assert stats["window_size"] == 10

def test_anomaly_detector_trigger_high_z_score():
    # An extreme outlier > 3 sigma
    alerts = anom_detector.observe("sensor_test", {"area_delta": 999.0})
    assert isinstance(alerts, list)

def test_alert_dispatcher_registration():
    url = "https://discord.com/api/webhooks/test/123"
    alert_dispatcher.register(url)
    stats = alert_dispatcher.get_stats()
    assert stats["registered_webhooks"] >= 1
    assert url in stats["webhook_urls"]


# =====================================================================
# 4. Pipeline Health Monitor Tests
# =====================================================================
def test_pipeline_health_report():
    report = health_monitor.get_full_report(query_store, anom_detector, alert_dispatcher)
    assert "status" in report
    assert "database" in report
    assert "anomaly_detector" in report
    assert "components" in report
    assert report["database"]["query_count"] >= 1


# =====================================================================
# 5. AI Digest Generator Tests
# =====================================================================
def test_digest_rule_based_generation():
    analytics = raster_engine.compute_change_analytics("dubai_urban")
    digest = digest_generator.generate("dubai_urban", analytics)
    assert "digest" in digest
    assert "Dubai Urban" in digest["digest"]
    assert digest["mode"] in ["GEMINI_LLM", "RULE_BASED"]
    assert digest["preset_id"] == "dubai_urban"

def test_digest_caching():
    analytics = raster_engine.compute_change_analytics("dubai_urban")
    digest1 = digest_generator.generate("dubai_urban", analytics)
    digest2 = digest_generator.generate("dubai_urban", analytics)
    assert digest2["cached"] is True
