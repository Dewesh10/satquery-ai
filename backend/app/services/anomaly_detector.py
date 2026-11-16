"""
anomaly_detector.py — Z-score rolling-baseline change anomaly detector.
Modeled after PulseLite's 3x rolling-average rule, adapted for geospatial NDVI/NDWI deltas.

Detects:
- DEFORESTATION_SPIKE: NDVI delta drops sharply below seasonal baseline
- FLOOD_INUNDATION: NDWI delta spikes far above baseline  
- URBAN_BURST: NDBI delta rises sharply (new built-up area)
- WATER_LOSS_CRITICAL: NDWI drops below multi-year low

Thresholds:
- |Z| > 3.0 → CRITICAL
- |Z| > 2.5 → WARNING  
- |Z| > 2.0 → INFO
"""
import time
import uuid
from typing import Dict, List, Any, Optional

# Rolling baseline window (number of observations to keep)
BASELINE_WINDOW = 10

# Severity thresholds (Z-score magnitude)
THRESHOLDS = {
    "CRITICAL": 3.0,
    "WARNING": 2.5,
    "INFO": 2.0
}

ALERT_TYPE_MAP = {
    "ndvi_delta": {"negative": "DEFORESTATION_SPIKE", "positive": "VEGETATION_RECOVERY"},
    "ndwi_delta": {"positive": "FLOOD_INUNDATION", "negative": "WATER_LOSS_CRITICAL"},
    "ndbi_delta": {"positive": "URBAN_BURST", "negative": "URBAN_REMOVAL"},
    "area_delta": {"positive": "CHANGE_AREA_SPIKE", "negative": "CHANGE_AREA_COLLAPSE"}
}

class ChangeAnomalyDetector:
    """
    Rolling Z-score anomaly detector for satellite change metrics.
    Maintains an in-memory rolling window per preset_id per metric.
    Z = (current - mean(window)) / std(window)
    Fires alert if |Z| > threshold.
    """
    def __init__(self):
        # Rolling windows: {preset_id: {metric: [values]}}
        self._windows: Dict[str, Dict[str, List[float]]] = {}
        # Active alerts: list of alert dicts
        self._alerts: List[Dict[str, Any]] = []

    def _get_window(self, preset_id: str, metric: str) -> List[float]:
        return self._windows.setdefault(preset_id, {}).setdefault(metric, [])

    def _compute_z(self, value: float, window: List[float]) -> Optional[float]:
        """Compute Z-score of value against window. Returns None if window too small."""
        if len(window) < 3:
            return None  # Not enough history yet
        import math
        mean = sum(window) / len(window)
        variance = sum((x - mean) ** 2 for x in window) / len(window)
        std = math.sqrt(variance) + 1e-9
        return (value - mean) / std

    def _get_severity(self, z_abs: float) -> Optional[str]:
        if z_abs >= THRESHOLDS["CRITICAL"]:
            return "CRITICAL"
        elif z_abs >= THRESHOLDS["WARNING"]:
            return "WARNING"
        elif z_abs >= THRESHOLDS["INFO"]:
            return "INFO"
        return None

    def _get_alert_type(self, metric: str, z: float) -> str:
        direction = "positive" if z > 0 else "negative"
        return ALERT_TYPE_MAP.get(metric, {}).get(direction, "CHANGE_ANOMALY")

    def observe(self, preset_id: str, metrics: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Feed new metric observations. Returns list of triggered alerts.
        Call this after each analytics computation.
        """
        triggered = []
        for metric, value in metrics.items():
            window = self._get_window(preset_id, metric)
            z = self._compute_z(value, window)

            # Update rolling window
            window.append(value)
            if len(window) > BASELINE_WINDOW:
                window.pop(0)

            if z is None:
                continue

            severity = self._get_severity(abs(z))
            if severity is None:
                continue

            alert_type = self._get_alert_type(metric, z)
            alert_id = f"ALT-{uuid.uuid4().hex[:8].upper()}"
            alert = {
                "alert_id": alert_id,
                "preset_id": preset_id,
                "alert_type": alert_type,
                "metric": metric,
                "observed_value": round(value, 4),
                "z_score": round(z, 3),
                "severity": severity,
                "threshold_used": THRESHOLDS[severity],
                "message": (
                    f"{alert_type} detected for {preset_id}: "
                    f"{metric}={round(value,3)} (Z={round(z,2)}, {severity})"
                ),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
            }
            self._alerts.insert(0, alert)
            triggered.append(alert)

        # Keep alert list bounded
        self._alerts = self._alerts[:200]
        return triggered

    def get_alerts(self, limit: int = 50) -> List[Dict]:
        return self._alerts[:limit]

    def get_stats(self) -> Dict:
        total = len(self._alerts)
        by_severity = {"CRITICAL": 0, "WARNING": 0, "INFO": 0}
        for a in self._alerts:
            by_severity[a.get("severity", "INFO")] = by_severity.get(a.get("severity", "INFO"), 0) + 1
        last_alert_ts = self._alerts[0]["timestamp"] if self._alerts else None
        return {
            "total_alerts": total,
            "by_severity": by_severity,
            "last_alert_timestamp": last_alert_ts,
            "presets_monitored": list(self._windows.keys()),
            "window_size": BASELINE_WINDOW
        }

anom_detector = ChangeAnomalyDetector()
