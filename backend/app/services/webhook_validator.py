"""
webhook_validator.py — Webhook URL allowlist for safe outbound dispatch.

Prevents Server-Side Request Forgery (SSRF): without this check, any user could
register a URL like http://169.254.169.254/latest/meta-data/ (AWS metadata endpoint),
http://localhost:5432/ (internal Postgres), or any internal host, and make
the server exfiltrate data or probe private services.

Allowed domains (extend as needed):
  - Discord webhooks: discord.com, discordapp.com
  - Slack webhooks: hooks.slack.com
  - Custom public host via ALLOWED_WEBHOOK_DOMAINS env var (comma-separated)

Usage:
    from app.services.webhook_validator import validate_webhook_url
    validate_webhook_url(url)   # raises ValueError if disallowed
"""

import os
import re
from urllib.parse import urlparse

# Hard-coded safe vendor domains
_HARDCODED_ALLOWED_DOMAINS = {
    "discord.com",
    "discordapp.com",
    "hooks.slack.com",
    "slack.com",
}

# Operator-added domains via environment variable (e.g. "mymonitoring.example.com,alerts.corp.com")
_env_domains = os.getenv("ALLOWED_WEBHOOK_DOMAINS", "")
_EXTRA_DOMAINS = {d.strip().lower() for d in _env_domains.split(",") if d.strip()}

ALLOWED_DOMAINS = _HARDCODED_ALLOWED_DOMAINS | _EXTRA_DOMAINS

# Patterns that must never appear in allowed URLs regardless of hostname
_BLOCKED_PATTERNS = re.compile(
    r"(localhost|127\.\d+\.\d+\.\d+|0\.0\.0\.0|::1|"
    r"169\.254\.\d+\.\d+|"      # AWS / GCP / Azure metadata
    r"192\.168\.\d+\.\d+|"      # RFC-1918 private
    r"10\.\d+\.\d+\.\d+|"       # RFC-1918 private
    r"172\.(1[6-9]|2[0-9]|3[01])\.\d+\.\d+)",  # RFC-1918 private
    re.IGNORECASE,
)


def validate_webhook_url(url: str) -> str:
    """
    Validate a webhook URL against the domain allowlist.

    Returns the URL unchanged if valid.
    Raises ValueError with a user-safe message if invalid.
    """
    if not url or not isinstance(url, str):
        raise ValueError("Webhook URL must be a non-empty string")

    url = url.strip()

    # Must be HTTPS (no plaintext HTTP for outbound secrets)
    if not url.startswith("https://"):
        raise ValueError(
            "Webhook URL must use HTTPS. "
            "Plaintext HTTP is not allowed for security reasons."
        )

    # Block any private / loopback / metadata address patterns in the raw URL
    if _BLOCKED_PATTERNS.search(url):
        raise ValueError(
            "Webhook URL resolves to a private or reserved address. "
            "Only public internet URLs are allowed."
        )

    parsed = urlparse(url)
    hostname = (parsed.hostname or "").lower()

    # Strip port and check the registered domain suffix
    # e.g. "discord.com" matches "ptb.discord.com", "canary.discord.com"
    allowed = any(
        hostname == domain or hostname.endswith("." + domain)
        for domain in ALLOWED_DOMAINS
    )

    if not allowed:
        raise ValueError(
            f"Webhook domain '{hostname}' is not on the allowlist. "
            f"Permitted domains: {sorted(ALLOWED_DOMAINS)}. "
            "To add a custom domain, set the ALLOWED_WEBHOOK_DOMAINS env var."
        )

    return url
