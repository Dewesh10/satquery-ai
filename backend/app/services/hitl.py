import time
from typing import Dict, List, Any

class HITLFeedbackService:
    def __init__(self):
        self.feedback_log: List[Dict[str, Any]] = []

    def submit_correction(self, feature_id: str, feedback_type: str, user_comment: str, corrected_coords: List[float] = None) -> Dict[str, Any]:
        record = {
            "feedback_id": f"HITL-{len(self.feedback_log)+1:04d}",
            "feature_id": feature_id,
            "feedback_type": feedback_type, # 'FALSE_POSITIVE', 'FALSE_NEGATIVE', 'BOUNDARY_CORRECTION'
            "user_comment": user_comment,
            "corrected_coords": corrected_coords,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "status": "QUEUED_FOR_RETRAINING"
        }
        self.feedback_log.append(record)
        return record

    def get_feedback_logs(self) -> List[Dict[str, Any]]:
        return self.feedback_log

hitl_service = HITLFeedbackService()
