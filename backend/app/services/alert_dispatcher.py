"""
alert_dispatcher.py — Real HTTP webhook dispatcher with retry/backoff.
Fires POST to Discord/Slack/custom URLs when anomaly detector triggers.
Modeled after PulseLite's Discord webhook alerts.
"""
import urllib.request
import json
import time
import os
from typing import Dict, List, Any, Optional

WEBHOOK_URLS_ENV = os.getenv("SATQUERY_WEBHOOK_URLS", "")  # comma-separated
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")  # optional Discord-specific

MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 1.5  # seconds

class AlertDispatcher:
    def __init__(self):
        self._delivery_log: List[Dict] = []
        self._registered_webhooks: List[str] = []
        # Load from env on startup
        if DISCORD_WEBHOOK_URL:
            self._registered_webhooks.append(DISCORD_WEBHOOK_URL)
        for url in WEBHOOK_URLS_ENV.split(","):
            url = url.strip()
            if url:
                self._registered_webhooks.append(url)

    def register(self, url: str):
        if url not in self._registered_webhooks:
            self._registered_webhooks.append(url)

    def _build_discord_payload(self, alert: Dict) -> Dict:
        """Build Discord-compatible webhook payload."""
        severity_emoji = {"CRITICAL": "🚨", "WARNING": "⚠️", "INFO": "ℹ️"}.get(alert.get("severity"), "🔔")
        return {
            "username": "SatQuery AI Sentinel",
            "embeds": [{
                "title": f"{severity_emoji} {alert.get('alert_type', 'ANOMALY')} — {alert.get('preset_id', 'Unknown')}",
                "description": alert.get("message", ""),
                "color": {"CRITICAL": 15158332, "WARNING": 15844367, "INFO": 3447003}.get(alert.get("severity"), 0),
                "fields": [
                    {"name": "Metric", "value": alert.get("metric", "N/A"), "inline": True},
                    {"name": "Z-Score", "value": str(alert.get("z_score", "N/A")), "inline": True},
                    {"name": "Severity", "value": alert.get("severity", "N/A"), "inline": True},
                ],
                "footer": {"text": f"SatQuery AI | {alert.get('timestamp', '')}"},
            }]
        }

    def _build_generic_payload(self, alert: Dict) -> Dict:
        return {
            "event": "SATQUERY_ANOMALY_ALERT",
            "alert_id": alert.get("alert_id"),
            "preset_id": alert.get("preset_id"),
            "alert_type": alert.get("alert_type"),
            "severity": alert.get("severity"),
            "message": alert.get("message"),
            "z_score": alert.get("z_score"),
            "timestamp": alert.get("timestamp")
        }

    def dispatch(self, alert: Dict) -> List[Dict]:
        """Dispatch alert to all registered webhooks. Returns delivery receipts."""
        receipts = []
        for url in self._registered_webhooks:
            is_discord = "discord.com/api/webhooks" in url
            payload = self._build_discord_payload(alert) if is_discord else self._build_generic_payload(alert)
            receipt = self._post_with_retry(url, payload)
            receipts.append(receipt)
            self._delivery_log.insert(0, receipt)
        self._delivery_log = self._delivery_log[:100]
        return receipts

    def _post_with_retry(self, url: str, payload: Dict) -> Dict:
        """POST with exponential backoff retry."""
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                data = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(
                    url, data=data,
                    headers={"Content-Type": "application/json", "User-Agent": "SatQueryAI-Sentinel/2.0"},
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=5) as resp:
                    return {
                        "url": url, "status_code": resp.status,
                        "attempt": attempt, "success": True,
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
                    }
            except Exception as e:
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_BACKOFF_BASE ** attempt)
                else:
                    return {
                        "url": url, "status_code": None,
                        "attempt": attempt, "success": False,
                        "error": str(e),
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
                    }
        return {"url": url, "success": False}

    def get_delivery_log(self, limit: int = 20) -> List[Dict]:
        return self._delivery_log[:limit]

    def get_stats(self) -> Dict:
        total = len(self._delivery_log)
        successes = sum(1 for r in self._delivery_log if r.get("success"))
        return {
            "registered_webhooks": len(self._registered_webhooks),
            "webhook_urls": self._registered_webhooks,
            "total_deliveries": total,
            "successful_deliveries": successes,
            "failed_deliveries": total - successes,
            "last_delivery": self._delivery_log[0] if self._delivery_log else None
        }

alert_dispatcher = AlertDispatcher()
