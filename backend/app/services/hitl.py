import time
import os
import sqlite3
from typing import Dict, List, Any

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "satquery_history.db")

class HITLFeedbackService:
    def __init__(self):
        self._init_db()

    def _init_db(self):
        try:
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS hitl_feedback (
                        feedback_id TEXT PRIMARY KEY,
                        feature_id TEXT NOT NULL,
                        feedback_type TEXT NOT NULL,
                        user_comment TEXT,
                        timestamp TEXT NOT NULL,
                        status TEXT NOT NULL
                    )
                """)
                conn.commit()
        except Exception:
            pass

    def submit_correction(self, feature_id: str, feedback_type: str, user_comment: str, corrected_coords: List[float] = None) -> Dict[str, Any]:
        feedback_id = f"HITL-{int(time.time()*1000)%1000000:06d}"
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ")
        record = {
            "feedback_id": feedback_id,
            "feature_id": feature_id,
            "feedback_type": feedback_type, # 'FALSE_POSITIVE', 'FALSE_NEGATIVE', 'BOUNDARY_CORRECTION'
            "user_comment": user_comment,
            "corrected_coords": corrected_coords,
            "timestamp": now,
            "status": "STORED_FOR_THRESHOLD_CALIBRATION"
        }
        
        try:
            with sqlite3.connect(DB_PATH) as conn:
                conn.execute(
                    "INSERT INTO hitl_feedback (feedback_id, feature_id, feedback_type, user_comment, timestamp, status) VALUES (?, ?, ?, ?, ?, ?)",
                    (feedback_id, feature_id, feedback_type, user_comment, now, record["status"])
                )
                conn.commit()
        except Exception:
            pass

        return record

    def get_feedback_logs(self) -> List[Dict[str, Any]]:
        logs = []
        try:
            with sqlite3.connect(DB_PATH) as conn:
                rows = conn.execute("SELECT feedback_id, feature_id, feedback_type, user_comment, timestamp, status FROM hitl_feedback ORDER BY timestamp DESC LIMIT 50").fetchall()
                for r in rows:
                    logs.append({
                        "feedback_id": r[0],
                        "feature_id": r[1],
                        "feedback_type": r[2],
                        "user_comment": r[3],
                        "timestamp": r[4],
                        "status": r[5]
                    })
        except Exception:
            pass
        return logs

    def get_active_threshold_tuning_recommendation(self) -> Dict[str, Any]:
        """Analyzes user feedback to suggest threshold tuning."""
        logs = self.get_feedback_logs()
        fp_count = sum(1 for l in logs if l.get("feedback_type") == "FALSE_POSITIVE")
        fn_count = sum(1 for l in logs if l.get("feedback_type") == "FALSE_NEGATIVE")
        
        recommendation = "Threshold balanced."
        adj = 0.0
        if fp_count > fn_count:
            recommendation = f"High false positive rate detected ({fp_count} reports). Recommend raising threshold by +0.05 to filter noise."
            adj = +0.05
        elif fn_count > fp_count:
            recommendation = f"Missed changes reported ({fn_count} reports). Recommend lowering threshold by -0.05 to increase sensitivity."
            adj = -0.05
            
        return {
            "total_feedback_count": len(logs),
            "false_positives": fp_count,
            "false_negatives": fn_count,
            "recommended_threshold_adjustment": adj,
            "guidance": recommendation
        }

hitl_service = HITLFeedbackService()
