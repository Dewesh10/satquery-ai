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
        self.webhooks: List[Dict[str, Any]] = [
            {
                "webhook_id": "WHK-001",
                "url": "https://api.disaster-management.gov.in/webhooks/sentinel",
                "min_severity": "CRITICAL",
                "status": "HEALTHY",
                "last_dispatch": "2024-02-20T06:40:22Z"
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

    def get_webhooks(self) -> List[Dict[str, Any]]:
        return self.webhooks

    def register_webhook(self, url: str, min_severity: str = "WARNING") -> Dict[str, Any]:
        webhook = {
            "webhook_id": f"WHK-{len(self.webhooks)+1:03d}",
            "url": url,
            "min_severity": min_severity,
            "status": "ACTIVE",
            "last_dispatch": "NEVER"
        }
        self.webhooks.append(webhook)
        return webhook

    def trigger_simulated_alert(self, watchlist_id: str, severity: str = "CRITICAL", custom_message: str = None) -> Dict[str, Any]:
        watchlist = next((w for w in self.watchlists if w["id"] == watchlist_id), self.watchlists[0])
        alert_count = sum(len(w.get("active_alerts", [])) for w in self.watchlists)
        alert_id = f"ALT-{904 + alert_count}"
        
        new_alert = {
            "alert_id": alert_id,
            "severity": severity,
            "title": f"Automated Satellite Orbit Breach: {watchlist['name']}",
            "change_delta": "+12.8 sq km threshold breach",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "coordinates": [92.60, 26.25] if watchlist["preset_id"] == "assam_flood" else [55.16, 24.99],
            "message": custom_message or f"Real-time orbit pass trigger for {watchlist['name']} breached alert threshold ({watchlist['threshold']})."
        }
        watchlist["active_alerts"].insert(0, new_alert)
        
        # Dispatch webhook notification simulation
        dispatched_webhooks = []
        for wh in self.webhooks:
            wh["last_dispatch"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
            dispatched_webhooks.append({
                "webhook_id": wh["webhook_id"],
                "url": wh["url"],
                "status_code": 200,
                "payload_delivered": {
                    "event": "SENTINEL_THRESHOLD_ALERT",
                    "alert": new_alert
                }
            })
            
        return {
            "status": "ALERT_TRIGGERED_AND_DISPATCHED",
            "alert": new_alert,
            "dispatched_webhooks": dispatched_webhooks
        }

sentinel_monitor = SentinelMonitorService()
