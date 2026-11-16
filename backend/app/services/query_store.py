"""
query_store.py — SQLite-backed query history & session replay.
Modeled after PulseLite's CSV persistence approach but using SQLite for structured queries.
"""
import sqlite3
import json
import time
import os
from typing import Dict, List, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "satquery_history.db")

DEMO_SNAPSHOT = [
    # Pre-recorded demo queries — timestamps are shifted to "now" on every load
    # so it always looks live even if run weeks later (same approach as PulseLite Demo Mode)
    {"run_id": "DEMO-RUN-001", "query": "Show built-up growth in Dubai between 2018 and 2024", "preset_id": "dubai_urban", "area_sq_km": 42.8, "percentage_change": "+18.4%", "confidence": 0.942},
    {"run_id": "DEMO-RUN-002", "query": "Detect canopy loss in Amazon Basin July 2020-2024", "preset_id": "amazon_deforestation", "area_sq_km": 68.5, "percentage_change": "-12.6%", "confidence": 0.961},
    {"run_id": "DEMO-RUN-003", "query": "Analyze flood inundation in Assam monsoon July 2023", "preset_id": "assam_flood", "area_sq_km": 114.6, "percentage_change": "+310.5%", "confidence": 0.938},
    {"run_id": "DEMO-RUN-004", "query": "Lake Mead water body shrinkage 2015 to 2023", "preset_id": "lake_mead", "area_sq_km": 31.2, "percentage_change": "-24.1%", "confidence": 0.955},
    {"run_id": "DEMO-RUN-005", "query": "Singapore port vessel traffic analysis June 2024", "preset_id": "singapore_maritime", "area_sq_km": 18.5, "percentage_change": "+14.2%", "confidence": 0.978},
]

class QueryStore:
    def __init__(self):
        self._init_db()

    def _init_db(self):
        """Create tables if they don't exist."""
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS query_history (
                    run_id TEXT PRIMARY KEY,
                    query TEXT NOT NULL,
                    preset_id TEXT NOT NULL,
                    area_sq_km REAL,
                    percentage_change TEXT,
                    confidence REAL,
                    plan_json TEXT,
                    analytics_json TEXT,
                    evidence_json TEXT,
                    created_at REAL NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS alert_log (
                    alert_id TEXT PRIMARY KEY,
                    preset_id TEXT NOT NULL,
                    alert_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    metric_value REAL,
                    threshold REAL,
                    message TEXT,
                    webhook_delivered INTEGER DEFAULT 0,
                    created_at REAL NOT NULL
                )
            """)
            conn.commit()

    def save_run(self, run_id: str, plan: Dict, analytics: Dict, evidence: Dict) -> Dict:
        """Persist a query run to SQLite and return timeline."""
        timeline = []
        now = time.time()
        for idx, step in enumerate(plan.get("dag_steps", [])):
            timeline.append({
                "step_index": idx,
                "step_id": step["step_id"],
                "name": step["name"],
                "tool": step["tool"],
                "timestamp_ms": int((now + idx * 0.4) * 1000),
                "duration_ms": 320 + (idx * 45),
                "status": "SUCCESS",
                "details": step["output"]
            })

        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                """INSERT OR REPLACE INTO query_history
                   (run_id, query, preset_id, area_sq_km, percentage_change, confidence,
                    plan_json, analytics_json, evidence_json, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    run_id,
                    plan.get("query", ""),
                    plan.get("selected_preset_id", ""),
                    analytics.get("area_sq_km", 0.0),
                    analytics.get("percentage_change", "0%"),
                    analytics.get("confidence_score", 0.0),
                    json.dumps(plan),
                    json.dumps(analytics),
                    json.dumps(evidence),
                    now
                )
            )
            conn.commit()

        run_record = {
            "run_id": run_id,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)),
            "query": plan.get("query"),
            "preset_id": plan.get("selected_preset_id"),
            "timeline": timeline,
            "analytics": analytics,
            "evidence": evidence
        }
        return run_record

    def get_run(self, run_id: str) -> Optional[Dict]:
        """Retrieve a specific run by ID (or from demo snapshot)."""
        # Check demo snapshot first
        for demo in DEMO_SNAPSHOT:
            if demo["run_id"] == run_id:
                return self._make_demo_run(demo)

        with sqlite3.connect(DB_PATH) as conn:
            row = conn.execute(
                "SELECT run_id, query, preset_id, plan_json, analytics_json, evidence_json, created_at FROM query_history WHERE run_id=?",
                (run_id,)
            ).fetchone()
        if not row:
            return None
        return {
            "run_id": row[0], "query": row[1], "preset_id": row[2],
            "plan": json.loads(row[3]), "analytics": json.loads(row[4]),
            "evidence": json.loads(row[5]),
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(row[6]))
        }

    def get_history(self, limit: int = 20) -> List[Dict]:
        """Return the last N query runs, newest first."""
        rows = []
        with sqlite3.connect(DB_PATH) as conn:
            rows = conn.execute(
                """SELECT run_id, query, preset_id, area_sq_km, percentage_change, confidence, created_at
                   FROM query_history ORDER BY created_at DESC LIMIT ?""",
                (limit,)
            ).fetchall()
        return [
            {"run_id": r[0], "query": r[1], "preset_id": r[2],
             "area_sq_km": r[3], "percentage_change": r[4], "confidence": r[5],
             "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(r[6]))}
            for r in rows
        ]

    def get_db_stats(self) -> Dict:
        """Return SQLite stats for pipeline health dashboard."""
        try:
            with sqlite3.connect(DB_PATH) as conn:
                query_count = conn.execute("SELECT COUNT(*) FROM query_history").fetchone()[0]
                alert_count = conn.execute("SELECT COUNT(*) FROM alert_log").fetchone()[0]
                last_query_ts = conn.execute("SELECT MAX(created_at) FROM query_history").fetchone()[0]
            db_size_bytes = os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 0
            return {
                "query_count": query_count,
                "alert_count": alert_count,
                "last_query_ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(last_query_ts)) if last_query_ts else None,
                "db_size_bytes": db_size_bytes,
                "db_path": DB_PATH
            }
        except Exception as e:
            return {"error": str(e)}

    def save_alert(self, alert_id: str, preset_id: str, alert_type: str, severity: str,
                   metric_value: float, threshold: float, message: str, webhook_delivered: bool = False):
        """Persist an anomaly alert to the alert_log table."""
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                """INSERT OR REPLACE INTO alert_log
                   (alert_id, preset_id, alert_type, severity, metric_value, threshold, message, webhook_delivered, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (alert_id, preset_id, alert_type, severity, metric_value, threshold, message, int(webhook_delivered), time.time())
            )
            conn.commit()

    def get_alert_history(self, limit: int = 50) -> List[Dict]:
        with sqlite3.connect(DB_PATH) as conn:
            rows = conn.execute(
                "SELECT alert_id, preset_id, alert_type, severity, metric_value, threshold, message, webhook_delivered, created_at FROM alert_log ORDER BY created_at DESC LIMIT ?",
                (limit,)
            ).fetchall()
        return [
            {"alert_id": r[0], "preset_id": r[1], "alert_type": r[2], "severity": r[3],
             "metric_value": r[4], "threshold": r[5], "message": r[6],
             "webhook_delivered": bool(r[7]),
             "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(r[8]))}
            for r in rows
        ]

    def get_demo_snapshot(self) -> List[Dict]:
        """Return demo snapshot with timestamps shifted to now (like PulseLite Demo Mode)."""
        now = time.time()
        result = []
        for i, demo in enumerate(DEMO_SNAPSHOT):
            shifted_time = now - (len(DEMO_SNAPSHOT) - i) * 300  # 5 min apart
            result.append({
                **demo,
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(shifted_time)),
                "demo_mode": True
            })
        return result

    def _make_demo_run(self, demo: Dict) -> Dict:
        """Construct a full run response from a demo snapshot entry."""
        return {
            "run_id": demo["run_id"],
            "query": demo["query"],
            "preset_id": demo["preset_id"],
            "demo_mode": True,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "analytics": {"preset_id": demo["preset_id"], "area_sq_km": demo["area_sq_km"],
                          "percentage_change": demo["percentage_change"], "confidence_score": demo["confidence"],
                          "data_source": "SIMULATED"},
        }

query_store = QueryStore()
