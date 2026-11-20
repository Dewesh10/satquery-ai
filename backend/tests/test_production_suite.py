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
from app.services.cloud_mask import apply_scl_cloud_mask
from app.services.timeseries import timeseries_engine
from app.services.reproducibility import generate_reproducibility_manifest

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
    assert bm["metrics"]["iou_jaccard"] > 0.50
    assert bm["metrics"]["recall"] > 0.80

def test_oscd_urban_evaluation():
    bm = evaluate_oscd_urban(threshold_delta=0.28)
    assert "metrics" in bm
    assert bm["metrics"]["f1_score"] >= 0.40
    assert bm["metrics"]["recall"] > 0.60

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

# =====================================================================
# 9. Cloud Masking, Multi-Date Time Series & Reproducibility Tests
# =====================================================================
def test_scl_cloud_masking():
    import numpy as np
    band = np.ones((10, 10))
    scl = np.full((10, 10), 4) # 4 = vegetation (valid)
    scl[2:5, 2:5] = 9          # 9 = cloud high prob (masked)
    scl[0, 0] = 3              # 3 = cloud shadow (masked)
    masked_band, stats = apply_scl_cloud_mask(band, scl)
    assert stats["cloud_shadow_pixels"] == 10
    assert stats["valid_pixels"] == 90
    assert stats["cloud_free_fraction"] == 0.90
    assert np.isnan(masked_band[0, 0])
    assert masked_band[5, 5] == 1.0

def test_timeseries_analysis():
    ts = timeseries_engine.compute_timeseries("dubai_urban")
    assert ts["preset_id"] == "dubai_urban"
    assert "trend_summary" in ts
    assert ts["trend_summary"]["slope_per_observation"] > 0
    assert len(ts["time_series_observations"]) >= 5
    assert "cloud_free_fraction" in ts["time_series_observations"][0]

def test_reproducibility_manifest():
    manifest = generate_reproducibility_manifest(
        query_text="Assess Dubai urban growth",
        preset_id="dubai_urban",
        bbox=[55.0, 25.0, 55.3, 25.2],
        primary_metric="+18.4 sq km"
    )
    assert "reproducibility_hash_sha256" in manifest
    assert len(manifest["reproducibility_hash_sha256"]) == 64
    assert len(manifest["stac_input_scenes"]) == 2
    assert manifest["software_environment"]["name"] == "SatQuery AI"


# =====================================================================
# Security Tests
# =====================================================================

def test_safe_formula_eval_valid():
    """Safe parser correctly evaluates a standard NDVI formula."""
    import numpy as np
    from app.services.safe_formula_eval import safe_eval_formula

    rng = np.random.default_rng(1)
    bands = {
        'B02': rng.uniform(0.04, 0.12, (10, 10)),
        'B03': rng.uniform(0.06, 0.18, (10, 10)),
        'B04': rng.uniform(0.05, 0.22, (10, 10)),
        'B08': rng.uniform(0.25, 0.65, (10, 10)),
        'B11': rng.uniform(0.12, 0.35, (10, 10)),
        'B12': rng.uniform(0.08, 0.28, (10, 10)),
    }

    result = safe_eval_formula("(B08 - B04) / (B08 + B04)", bands)
    assert result.shape == (10, 10)
    assert result.min() >= -1.0
    assert result.max() <= 1.0


def test_safe_formula_eval_blocks_import():
    """Safe parser must reject __import__ or any non-arithmetic expression."""
    import numpy as np
    from app.services.safe_formula_eval import safe_eval_formula

    bands = {b: np.ones((5, 5)) for b in ['B02','B03','B04','B08','B11','B12']}

    # These should all raise ValueError or SyntaxError — never execute
    dangerous = [
        "__import__('os').system('id')",
        "open('/etc/passwd').read()",
        "[x for x in range(10)]",
        "B08 if True else B04",
        "B08 == B04",
    ]
    for expr in dangerous:
        try:
            safe_eval_formula(expr, bands)
            raise AssertionError(f"Should have raised for: {expr!r}")
        except (ValueError, SyntaxError):
            pass  # expected — blocked


def test_safe_formula_eval_blocks_unknown_name():
    """Safe parser must reject variable names that aren't band identifiers."""
    import numpy as np
    from app.services.safe_formula_eval import safe_eval_formula

    bands = {b: np.ones((5, 5)) for b in ['B02','B03','B04','B08','B11','B12']}

    with pytest.raises((ValueError, SyntaxError)):
        safe_eval_formula("os + B08", bands)


def test_webhook_validator_allows_discord():
    """Discord HTTPS URLs should pass validation."""
    from app.services.webhook_validator import validate_webhook_url

    url = "https://discord.com/api/webhooks/123456789/abcdefXYZ"
    assert validate_webhook_url(url) == url


def test_webhook_validator_allows_slack():
    """Slack HTTPS hook URLs should pass validation."""
    from app.services.webhook_validator import validate_webhook_url

    url = "https://hooks.slack.com/services/T000/B000/xxxx"
    assert validate_webhook_url(url) == url


def test_webhook_validator_blocks_localhost():
    """Localhost URLs must be rejected (SSRF prevention)."""
    from app.services.webhook_validator import validate_webhook_url

    with pytest.raises(ValueError, match="private|reserved|HTTPS"):
        validate_webhook_url("http://localhost:9200/exfiltrate")


def test_webhook_validator_blocks_internal_ip():
    """RFC-1918 private IPs must be rejected."""
    from app.services.webhook_validator import validate_webhook_url

    with pytest.raises(ValueError):
        validate_webhook_url("https://192.168.1.1/steal")


def test_webhook_validator_blocks_aws_metadata():
    """AWS metadata endpoint must be rejected."""
    from app.services.webhook_validator import validate_webhook_url

    with pytest.raises(ValueError):
        validate_webhook_url("https://169.254.169.254/latest/meta-data/")


def test_webhook_validator_blocks_plaintext_http():
    """HTTP (non-HTTPS) must be rejected regardless of domain."""
    from app.services.webhook_validator import validate_webhook_url

    with pytest.raises(ValueError, match="HTTPS"):
        validate_webhook_url("http://discord.com/api/webhooks/123/abc")


def test_webhook_validator_blocks_unknown_domain():
    """Unknown domains not on the allowlist must be rejected."""
    from app.services.webhook_validator import validate_webhook_url

    with pytest.raises(ValueError, match="allowlist"):
        validate_webhook_url("https://evil-attacker.com/steal-data")


def test_demo_seed_idempotent(tmp_path, monkeypatch):
    """Calling seed_demo_data() twice must not raise or duplicate rows."""
    import app.services.demo_seed as demo_seed_mod

    # Override DB path to a writable temp dir for the test environment
    test_db = str(tmp_path / "satquery_test.db")
    monkeypatch.setattr(demo_seed_mod, "DB_PATH", test_db)

    # Run twice — idempotency check
    demo_seed_mod.seed_demo_data()
    demo_seed_mod.seed_demo_data()

    # Verify rows were inserted exactly once
    import sqlite3
    conn = sqlite3.connect(test_db)
    hitl_count = conn.execute("SELECT COUNT(*) FROM hitl_feedback").fetchone()[0]
    alert_count = conn.execute("SELECT COUNT(*) FROM sentinel_alerts").fetchone()[0]
    conn.close()
    assert hitl_count == 4   # exactly 4 seed rows, not 8
    assert alert_count == 5  # exactly 5 seed rows, not 10
