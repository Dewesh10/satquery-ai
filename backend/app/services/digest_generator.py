"""
digest_generator.py — Geospatial AI Digest generator.
Uses Google Gemini API (free tier via AI Studio) if GEMINI_API_KEY is set.
Falls back to deterministic rule-based template if no API key — same design pattern
as PulseLite's Claude Haiku digest with rule-based fallback.

Configured via GEMINI_API_KEY environment variable.
Get a free key at: https://aistudio.google.com/app/apikey
"""
import urllib.request
import json
import os
import time
from typing import Dict, Any, Optional

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
# Default to current Gemini generation (gemini-2.5-flash / gemini-3.8-flash)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

class DigestGenerator:
    def __init__(self):
        self._cache: Dict[str, Dict] = {}  # {preset_id: {digest, timestamp}}
        self._using_llm = bool(GEMINI_API_KEY)

    def generate(self, preset_id: str, analytics: Dict, force_refresh: bool = False) -> Dict:
        """Generate or return cached digest for a preset."""
        # Return cache if fresh (< 5 minutes)
        cached = self._cache.get(preset_id)
        if cached and not force_refresh:
            age = time.time() - cached["cached_at"]
            if age < 300:  # 5 minutes, same as PulseLite
                return {**cached["digest"], "cached": True, "cache_age_seconds": int(age)}

        if GEMINI_API_KEY:
            digest = self._llm_digest(preset_id, analytics)
        else:
            digest = self._rule_based_digest(preset_id, analytics)

        self._cache[preset_id] = {"digest": digest, "cached_at": time.time()}
        return {**digest, "cached": False}

    def _llm_digest(self, preset_id: str, analytics: Dict) -> Dict:
        """Call Gemini 1.5 Flash (free tier) to generate narrative digest."""
        prompt = (
            f"You are a satellite intelligence analyst writing a brief situation report for a district collector or government officer.\n\n"
            f"Satellite Change Detection Results for: {preset_id.replace('_', ' ').title()}\n"
            f"- Primary metric: {analytics.get('primary_metric_label', 'Change Area')} = {analytics.get('primary_metric_value', 'N/A')}\n"
            f"- Percentage change: {analytics.get('percentage_change', 'N/A')}\n"
            f"- Area affected: {analytics.get('area_sq_km', 0):.1f} sq km ({analytics.get('hectares', 0)} hectares)\n"
            f"- Confidence score: {analytics.get('confidence_score', 0):.1%}\n"
            f"- Time period: {analytics.get('time_span', 'N/A')}\n\n"
            f"Write exactly 3 sentences: (1) What changed, (2) Why it matters for land management or disaster response, (3) Recommended immediate action. "
            f"Be specific, factual, and avoid speculation. Keep it under 100 words total."
        )

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.3, "maxOutputTokens": 150}
        }
        try:
            req = urllib.request.Request(
                url, data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return {
                    "digest": text.strip(),
                    "model": f"Gemini 1.5 Flash (Google AI Studio free tier)",
                    "mode": "LLM",
                    "preset_id": preset_id,
                    "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
                }
        except Exception as e:
            # LLM call failed — fall back to rule-based
            fallback = self._rule_based_digest(preset_id, analytics)
            fallback["llm_error"] = str(e)[:100]
            fallback["mode"] = "RULE_BASED_FALLBACK"
            return fallback

    def _rule_based_digest(self, preset_id: str, analytics: Dict) -> Dict:
        """Deterministic rule-based digest — always works without API key."""
        label = analytics.get("primary_metric_label", "Change")
        value = analytics.get("primary_metric_value", "N/A")
        pct = analytics.get("percentage_change", "0%")
        area = analytics.get("area_sq_km", 0)
        confidence = analytics.get("confidence_score", 0)
        time_span = analytics.get("time_span", "the analysis period")
        name = preset_id.replace("_", " ").title()

        # Determine change direction
        is_increase = pct.startswith("+") if isinstance(pct, str) else False
        is_decrease = pct.startswith("-") if isinstance(pct, str) else False

        # Category-based sentence templates
        if "deforestation" in preset_id or "amazon" in preset_id:
            sentence1 = f"Satellite analysis detected {value} of canopy loss across {name} during {time_span}."
            sentence2 = f"A {pct} change in forest cover ({area:.1f} sq km) indicates accelerating deforestation pressure on biodiversity and carbon sequestration capacity."
            sentence3 = "Recommend immediate cross-verification with INPE PRODES alerts and escalation to forestry enforcement authority."
        elif "flood" in preset_id or "assam" in preset_id:
            sentence1 = f"SAR radar analysis confirms {value} of active flood inundation in {name} during {time_span}."
            sentence2 = f"The {pct} surge in water body extent ({area:.1f} sq km) indicates high risk to agricultural livelihoods and infrastructure."
            sentence3 = "Recommend immediate evacuation advisory for low-lying settlements and coordination with State Disaster Management Authority."
        elif "urban" in preset_id or "dubai" in preset_id or "delhi" in preset_id or "mumbai" in preset_id:
            sentence1 = f"Optical satellite change detection identified {value} of new built-up area in {name} during {time_span}."
            sentence2 = f"A {pct} expansion ({area:.1f} sq km) indicates rapid urbanisation that may require land-use compliance verification."
            sentence3 = "Recommend cross-referencing with approved development plans and initiating field verification for encroachment screening."
        elif "water" in preset_id or "mead" in preset_id or "lake" in preset_id:
            sentence1 = f"Multi-temporal analysis shows {value} of water surface loss at {name} during {time_span}."
            sentence2 = f"A {pct} reduction in water extent ({area:.1f} sq km) signals critical drought stress and declining reservoir capacity."
            sentence3 = "Recommend immediate water resource audit and coordination with irrigation and drought management authorities."
        elif "maritime" in preset_id or "singapore" in preset_id:
            sentence1 = f"High-resolution SAR analysis detected {value} of vessel traffic activity in {name} during {time_span}."
            sentence2 = f"A {pct} change in maritime activity ({area:.1f} sq km monitored zone) indicates significant port logistics dynamics."
            sentence3 = "Recommend cross-checking with AIS vessel tracking data for berth occupancy compliance verification."
        else:
            sentence1 = f"Satellite change detection analysis of {name} for {time_span} identified {value} of spatial change."
            sentence2 = f"The {pct} shift ({area:.1f} sq km, confidence {confidence:.0%}) warrants administrative review of land-use patterns."
            sentence3 = "Recommend field verification and cross-referencing with district land records."

        digest_text = f"{sentence1} {sentence2} {sentence3}"
        return {
            "digest": digest_text,
            "model": "Rule-Based Template Engine (no API key required)",
            "mode": "RULE_BASED",
            "preset_id": preset_id,
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }

    def get_mode(self) -> str:
        return "LLM (Gemini 1.5 Flash)" if self._using_llm else "Rule-Based Fallback"

digest_generator = DigestGenerator()
