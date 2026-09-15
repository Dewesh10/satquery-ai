import time
from typing import Dict, List, Any

class ReplayStore:
    def __init__(self):
        self.runs: Dict[str, Dict[str, Any]] = {}

    def save_run(self, run_id: str, plan_data: Dict[str, Any], analytics_data: Dict[str, Any], evidence_data: Dict[str, Any]):
        timeline = []
        now = time.time()
        for idx, step in enumerate(plan_data.get("dag_steps", [])):
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
            
        self.runs[run_id] = {
            "run_id": run_id,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "query": plan_data.get("query"),
            "preset_id": plan_data.get("selected_preset_id"),
            "timeline": timeline,
            "analytics": analytics_data,
            "evidence": evidence_data
        }
        return self.runs[run_id]

    def get_run(self, run_id: str) -> Dict[str, Any]:
        return self.runs.get(run_id, None)

replay_store = ReplayStore()
