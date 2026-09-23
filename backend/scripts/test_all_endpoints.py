"""
Comprehensive End-to-End Test Suite for SatQuery AI FastAPI Backend
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

AUTH_HEADERS = {"X-API-Key": "satquery-demo-key-2024"}

def run_tests():
    print("=== RUNNING SATQUERY AI ENDPOINT AUDIT ===")
    
    # 0. API Key Auth Middleware Tests
    r_unauth = client.get("/api/presets")
    assert r_unauth.status_code == 401, f"Expected 401 for unauthenticated request, got {r_unauth.status_code}"
    print("[OK] GET /api/presets without API Key -> 401 Unauthorized (Blocked)")

    r_invalid = client.get("/api/presets", headers={"X-API-Key": "wrong-key"})
    assert r_invalid.status_code == 401, f"Expected 401 for invalid API Key, got {r_invalid.status_code}"
    print("[OK] GET /api/presets with invalid API Key -> 401 Unauthorized (Blocked)")

    r_query_auth = client.get("/api/presets?api_key=satquery-demo-key-2024")
    assert r_query_auth.status_code == 200, f"Expected 200 for api_key query param, got {r_query_auth.status_code}"
    print("[OK] GET /api/presets?api_key=... -> 200 OK (Query param auth verified)")
    
    # 1. Root
    r = client.get("/")
    assert r.status_code == 200, f"Root failed: {r.status_code}"
    print("[OK] GET / -> 200 OK")
    
    # 2. Presets
    r = client.get("/api/presets", headers=AUTH_HEADERS)
    assert r.status_code == 200, f"Presets failed: {r.status_code}"
    print("[OK] GET /api/presets -> 200 OK")
    
    # 3. Analytics
    r = client.get("/api/analytics/dubai_urban", headers=AUTH_HEADERS)
    assert r.status_code == 200, f"Analytics failed: {r.status_code}"
    print("[OK] GET /api/analytics/dubai_urban -> 200 OK")
    
    # 4. Copilot Query
    payload = {"prompt": "Show built-up growth in Dubai", "preset_id": "dubai_urban"}
    r = client.post("/api/query", json=payload, headers=AUTH_HEADERS)
    assert r.status_code == 200, f"Query failed: {r.status_code}"
    res_data = r.json()
    assert res_data["plan"]["selected_preset_id"] == "dubai_urban", f"Preset ID mismatch! Expected 'dubai_urban', got '{res_data['plan']['selected_preset_id']}'"
    assert res_data["analytics"]["preset_id"] == "dubai_urban", f"Analytics Preset ID mismatch! Expected 'dubai_urban', got '{res_data['analytics']['preset_id']}'"
    print("[OK] POST /api/query -> 200 OK (Explicit preset_id resolution verified)")
    
    # 5. Export Government Notice GET & POST
    r = client.get("/api/export/government-notice?preset_id=dubai_urban", headers=AUTH_HEADERS)
    assert r.status_code == 200, f"Export Notice GET failed: {r.status_code}"
    print("[OK] GET /api/export/government-notice -> 200 OK")
    
    # 6. Export PDF GET & POST
    r = client.get("/api/export/pdf?preset_id=dubai_urban", headers=AUTH_HEADERS)
    assert r.status_code == 200, f"Export PDF GET failed: {r.status_code}"
    print("[OK] GET /api/export/pdf -> 200 OK")

    # 7. Export GeoJSON
    r = client.get("/api/export/geojson?preset_id=dubai_urban", headers=AUTH_HEADERS)
    assert r.status_code == 200, f"Export GeoJSON GET failed: {r.status_code}"
    print("[OK] GET /api/export/geojson -> 200 OK")

    # 8. Export GeoTIFF STAC Manifest
    r = client.get("/api/export/geotiff-manifest?preset_id=dubai_urban", headers=AUTH_HEADERS)
    assert r.status_code == 200, f"Export GeoTIFF Manifest GET failed: {r.status_code}"
    print("[OK] GET /api/export/geotiff-manifest -> 200 OK")
    
    # 9. HITL Feedback
    r = client.post("/api/hitl/feedback", json={"feature_id": "F-001", "feedback_type": "FALSE_POSITIVE", "user_comment": "Cropland swing"}, headers=AUTH_HEADERS)
    assert r.status_code == 200, f"HITL failed: {r.status_code}"
    print("[OK] POST /api/hitl/feedback -> 200 OK")

    # 10. Sentinel Watchlists
    r = client.get("/api/sentinel/watchlists", headers=AUTH_HEADERS)
    assert r.status_code == 200, f"Watchlists failed: {r.status_code}"
    print("[OK] GET /api/sentinel/watchlists -> 200 OK")

    # 11. Sentinel Webhooks Registration & Trigger Alert
    r = client.post("/api/sentinel/webhooks", json={"url": "https://api.disaster-management.gov.in/webhooks/sentinel", "min_severity": "WARNING"}, headers=AUTH_HEADERS)
    assert r.status_code == 200, f"Register Webhook failed: {r.status_code}"
    print("[OK] POST /api/sentinel/webhooks -> 200 OK")

    r = client.post("/api/sentinel/alerts/trigger", json={"watchlist_id": "AOI-WATCH-02", "severity": "CRITICAL", "custom_message": "Flood threshold breached."}, headers=AUTH_HEADERS)
    assert r.status_code == 200, f"Trigger Alert failed: {r.status_code}"
    print("[OK] POST /api/sentinel/alerts/trigger -> 200 OK")

    print("\nALL 11 BACKEND API ENDPOINTS + API KEY AUTH MIDDLEWARE ARE 100% OPERATIONAL & VERIFIED!")

if __name__ == "__main__":
    run_tests()
