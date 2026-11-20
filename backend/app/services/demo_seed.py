"""
demo_seed.py — Load a minimal demo snapshot into SQLite on startup.

On ephemeral hosts (Railway, Fly.io) the filesystem resets on every redeploy,
so the SQLite alert log and HITL feedback history start empty. This module
seeds a few representative rows so the UI shows meaningful data immediately
after cold-start without needing any real prior queries.

Call seed_demo_data() once at application startup (see main.py lifespan).
The function is idempotent — it checks for existing rows before inserting.
"""

import sqlite3
import os
from datetime import datetime, timedelta, timezone

DB_PATH = os.getenv("SATQUERY_DB_PATH", "/app/data/satquery_history.db")


def _get_conn() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _ensure_tables(conn: sqlite3.Connection) -> None:
    """Create tables if they don't exist yet (mirrors hitl.py and sentinel_monitor.py schemas)."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS hitl_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feature_id TEXT NOT NULL,
            feedback_type TEXT NOT NULL,
            user_comment TEXT,
            corrected_coords TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS sentinel_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            watchlist_id TEXT NOT NULL,
            preset_id TEXT NOT NULL,
            z_score REAL,
            metric_value REAL,
            severity TEXT,
            alert_fired INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()


def seed_demo_data() -> None:
    """
    Insert representative demo rows so the UI renders data on cold start.
    Idempotent: skips insertion if rows already exist.
    """
    with _get_conn() as conn:
        _ensure_tables(conn)

        # --- HITL feedback seed ---
        existing_hitl = conn.execute("SELECT COUNT(*) FROM hitl_feedback").fetchone()[0]
        if existing_hitl == 0:
            now = datetime.now(timezone.utc)
            hitl_rows = [
                ("FEAT-DUBAI-001", "FALSE_POSITIVE",
                 "Road reflection misclassified as built-up expansion",
                 None,
                 (now - timedelta(days=14)).isoformat()),
                ("FEAT-DUBAI-002", "FALSE_NEGATIVE",
                 "Construction site on east boundary missed by NDBI threshold",
                 None,
                 (now - timedelta(days=10)).isoformat()),
                ("FEAT-ASSAM-001", "FALSE_POSITIVE",
                 "Seasonal river meander flagged as new flood event",
                 None,
                 (now - timedelta(days=7)).isoformat()),
                ("FEAT-DUBAI-003", "FALSE_NEGATIVE",
                 "Low-contrast concrete area not captured — suggest lower NDBI threshold",
                 None,
                 (now - timedelta(days=3)).isoformat()),
            ]
            conn.executemany(
                "INSERT INTO hitl_feedback (feature_id, feedback_type, user_comment, corrected_coords, created_at) "
                "VALUES (?, ?, ?, ?, ?)",
                hitl_rows
            )
            conn.commit()

        # --- Sentinel alert log seed ---
        existing_alerts = conn.execute("SELECT COUNT(*) FROM sentinel_alerts").fetchone()[0]
        if existing_alerts == 0:
            now = datetime.now(timezone.utc)
            alert_rows = [
                ("AOI-WATCH-01", "dubai_urban", 1.42, 51.8, "INFO",    0,
                 (now - timedelta(days=20)).isoformat()),
                ("AOI-WATCH-01", "dubai_urban", 2.17, 54.3, "WARNING", 0,
                 (now - timedelta(days=15)).isoformat()),
                ("AOI-WATCH-01", "dubai_urban", 3.85, 58.9, "CRITICAL", 1,
                 (now - timedelta(days=8)).isoformat()),
                ("AOI-WATCH-02", "assam_flood", 2.63, 182.4, "WARNING", 1,
                 (now - timedelta(days=5)).isoformat()),
                ("AOI-WATCH-01", "dubai_urban", 1.95, 60.5, "INFO",    0,
                 (now - timedelta(days=1)).isoformat()),
            ]
            conn.executemany(
                "INSERT INTO sentinel_alerts "
                "(watchlist_id, preset_id, z_score, metric_value, severity, alert_fired, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                alert_rows
            )
            conn.commit()

    print(f"[demo_seed] Demo data seeded into {DB_PATH}")
