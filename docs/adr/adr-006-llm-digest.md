# ADR-006 — AI Digest & Planner: Gemini 2.5 Flash with Deterministic Rule-Based Fallback

**Date**: 2024-11-05 (Updated 2025-05)  
**Status**: Accepted

## Context

SatQuery AI needs structured query compilation from natural language questions and human-readable narrative summaries of change detection results for non-technical users (district collectors, disaster management officers).

## Decision

Use **Google Gemini 2.5 Flash** (free tier via Google AI Studio) if `GEMINI_API_KEY` is set, with **strict JSON Schema validation** (`PLAN_JSON_SCHEMA`) for query planning and a **deterministic rule-based fallback** that always operates reliably without any API key.

## Rationale

Modeled after modern agentic microservices and PulseLite's tiered degradation pattern:

1. **Free tier & modern generation**: Gemini 2.5 Flash via Google AI Studio is fast, cost-free for prototyping, and provides high-fidelity structured JSON output.
2. **Schema-Validated Query Planning**: User prompts are compiled against a strict JSON schema (`region_name`, `start_date`, `end_date`, `sensor_modality`, `target_index`, `change_threshold`, `intent`), eliminating regex fragility while strictly rejecting hallucinated parameters.
3. **Graceful degradation**: Deterministic rule-based templates produce high-quality, category-specific digests and fallback plan compilation for all presets without requiring external network access.
4. **5-minute cache**: Digests are cached per preset for 5 minutes to avoid redundant API calls and respect quota boundaries.
5. **Honest attribution**: API responses clearly declare whether output is LLM-generated or rule-based fallback.
5. **Prompt engineering**: Instructs model to write exactly 3 sentences: (1) what changed, (2) why it matters, (3) recommended action — optimized for administrative decision-making.

## Get a Free API Key

https://aistudio.google.com/app/apikey — Free tier, no credit card required.

## Consequences

- **Positive**: Works without API key, transparent attribution, free in production at prototype scale.
- **Negative**: LLM outputs are non-deterministic (temperature=0.3 to reduce variance); rule-based is fully deterministic.
