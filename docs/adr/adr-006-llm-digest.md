# ADR-006 — AI Digest: Gemini 1.5 Flash with Rule-Based Fallback

**Date**: 2024-11-05  
**Status**: Accepted

## Context

SatQuery AI needs a human-readable narrative summary of change detection results for non-technical users (district collectors, disaster management officers).

## Decision

Use **Google Gemini 1.5 Flash** (free tier via AI Studio) if `GEMINI_API_KEY` is set, with a **deterministic rule-based fallback** that always works without any API key.

## Rationale

Modeled after PulseLite's Pulse Digest (Claude Haiku + rule-based fallback):

1. **Free tier**: Gemini 1.5 Flash via Google AI Studio is free for prototyping — no paid plan required.
2. **Graceful degradation**: Rule-based templates produce high-quality, category-specific digests for all 8 preset types. Zero API key needed.
3. **5-minute cache**: Digest is cached per preset for 5 minutes (same as PulseLite's refresh interval) to avoid redundant API calls.
4. **Honest attribution**: Response clearly states whether digest is LLM-generated or rule-based, so users always know what they're reading.
5. **Prompt engineering**: Instructs model to write exactly 3 sentences: (1) what changed, (2) why it matters, (3) recommended action — optimized for administrative decision-making.

## Get a Free API Key

https://aistudio.google.com/app/apikey — Free tier, no credit card required.

## Consequences

- **Positive**: Works without API key, transparent attribution, free in production at prototype scale.
- **Negative**: LLM outputs are non-deterministic (temperature=0.3 to reduce variance); rule-based is fully deterministic.
