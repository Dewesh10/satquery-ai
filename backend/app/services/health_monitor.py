"""
health_monitor.py — Pipeline health aggregator.
Provides latency pings, component status, and freshness badges.
Modeled after PulseLite's Pipeline Health tab.
"""
import urllib.request
import time
import sys
import os
from typing import Dict, Any

class PipelineHealthMonitor:
    def __init__(self):
        self._start_time = time.time()
        self._stac_latency_history: list = []  # last 10 pings ms
        self._osm_latency_history: list = []

    def _ping_url(self, url: str, timeout: float = 4.0) -> Dict:
        """Ping a URL and return latency_ms + status."""
        t0 = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "SatQueryAI-HealthCheck/2.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                latency_ms = round((time.time() - t0) * 1000, 1)
                return {"status": "UP", "latency_ms": latency_ms, "http_status": resp.status}
        except Exception as e:
            latency_ms = round((time.time() - t0) * 1000, 1)
            return {"status": "DOWN", "latency_ms": latency_ms, "error": str(e)[:100]}

    def check_stac_api(self) -> Dict:
        result = self._ping_url("https://earth-search.aws.element84.com/v1")
        self._stac_latency_history.append(result["latency_ms"])
        if len(self._stac_latency_history) > 10:
            self._stac_latency_history.pop(0)
        result["latency_history_ms"] = self._stac_latency_history[:]
        result["component"] = "Earth Search STAC API (AWS Element84)"
        return result

    def check_osm_geocoder(self) -> Dict:
        result = self._ping_url("https://nominatim.openstreetmap.org/status.php")
        self._osm_latency_history.append(result["latency_ms"])
        if len(self._osm_latency_history) > 10:
            self._osm_latency_history.pop(0)
        result["latency_history_ms"] = self._osm_latency_history[:]
        result["component"] = "OpenStreetMap Nominatim Geocoder"
        return result

    def get_full_report(self, query_store=None, anom_detector=None, alert_dispatcher=None) -> Dict:
        """Aggregate all health metrics into a single report."""
        uptime_seconds = round(time.time() - self._start_time)
        hours, rem = divmod(uptime_seconds, 3600)
        mins, secs = divmod(rem, 60)

        report = {
            "status": "OPERATIONAL",
            "uptime": f"{hours}h {mins}m {secs}s",
            "uptime_seconds": uptime_seconds,
            "python_version": sys.version.split()[0],
            "platform": sys.platform,
            "components": {
                "stac_api": self.check_stac_api(),
                "osm_geocoder": self.check_osm_geocoder(),
            },
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }

        if query_store:
            db_stats = query_store.get_db_stats()
            report["database"] = db_stats
            # Freshness badge: how long ago was the last query?
            last_ts = db_stats.get("last_query_ts")
            if last_ts:
                from datetime import datetime, timezone
                try:
                    last_dt = datetime.strptime(last_ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                    age_seconds = (datetime.now(timezone.utc) - last_dt).total_seconds()
                    if age_seconds < 60:
                        freshness = "LIVE"
                    elif age_seconds < 300:
                        freshness = "RECENT"
                    elif age_seconds < 3600:
                        freshness = "STALE"
                    else:
                        freshness = "COLD"
                    report["freshness"] = {"badge": freshness, "seconds_since_last_query": int(age_seconds)}
                except:
                    report["freshness"] = {"badge": "UNKNOWN"}
            else:
                report["freshness"] = {"badge": "NO_DATA"}

        if anom_detector:
            report["anomaly_detector"] = anom_detector.get_stats()

        if alert_dispatcher:
            report["webhook_dispatcher"] = alert_dispatcher.get_stats()

        # Set overall status based on components
        if any(c.get("status") == "DOWN" for c in report["components"].values()):
            report["status"] = "DEGRADED"

        return report

health_monitor = PipelineHealthMonitor()
