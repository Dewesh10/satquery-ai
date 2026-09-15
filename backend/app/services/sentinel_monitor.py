import time
from typing import Dict, List, Any

class SentinelMonitorService:
    def __init__(self):
        self.watchlists: List[Dict[str, Any]] = [
            {
                "id": "AOI-WATCH-01",
                "name": "Jebel Ali Coastal Construction Watch",
                "preset_id": "dubai_urban",
                "aoi_name": "Dubai Sector 4",
                "schedule": "Every 6 Hours (Sentinel-2 Pass)",
                "status": "ACTIVE_MONITORING",
                "last_run": "2024-02-20T06:00:00Z",
                "threshold": "> 5.0 sq km change",
                "active_alerts": [
                    {
                        "alert_id": "ALT-902",
                        "severity": "CRITICAL",
                        "title": "Unauthorized Construction Growth Detected",
                        "change_delta": "+18.4 sq km",
                        "timestamp": "2024-02-20T06:40:21Z",
                        "coordinates": [55.16, 24.99],
                        "message": "Encroachment threshold breached in Jebel Ali maritime corridor (+18.4 sq km growth)."
                    }
                ]
            },
            {
                "id": "AOI-WATCH-02",
                "name": "Brahmaputra Flood Plain Sentinel",
                "preset_id": "assam_flood",
                "aoi_name": "Assam Sector 2",
                "schedule": "Every 12 Hours (Sentinel-1 SAR Radar)",
                "status": "ACTIVE_MONITORING",
                "last_run": "2023-07-18T12:00:00Z",
                "threshold": "> 10.0 sq km inundation",
                "active_alerts": [
                    {
                        "alert_id": "ALT-903",
                        "severity": "EMERGENCY",
                        "title": "Monsoon Flood Inundation Spike",
                        "change_delta": "+114.6 sq km submerged",
                        "timestamp": "2023-07-18T11:55:42Z",
                        "coordinates": [92.60, 26.25],
                        "message": "Submerged agricultural land spiked by +310.5%. Emergency evacuation protocol advised."
                    }
                ]
            }
        ]

    def get_active_watchlists(self) -> List[Dict[str, Any]]:
        return self.watchlists

    def add_watchlist(self, name: str, preset_id: str, threshold: str) -> Dict[str, Any]:
        item = {
            "id": f"AOI-WATCH-{len(self.watchlists)+1:02d}",
            "name": name,
            "preset_id": preset_id,
            "aoi_name": "User Defined AOI",
            "schedule": "Every 6 Hours (Automatic Satellite Orbit Pass)",
            "status": "ACTIVE_MONITORING",
            "last_run": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "threshold": threshold,
            "active_alerts": []
        }
        self.watchlists.append(item)
        return item

sentinel_monitor = SentinelMonitorService()
