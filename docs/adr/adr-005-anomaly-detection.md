# ADR-005 — Anomaly Detection: Z-Score Rolling Baseline

**Date**: 2024-11-05  
**Status**: Accepted

## Context

SatQuery AI needs to automatically detect when change metrics deviate significantly from historical norms.

## Decision

Use a **Z-score rolling baseline anomaly detector** (window size 10, thresholds: 2.0σ INFO, 2.5σ WARNING, 3.0σ CRITICAL).

## Rationale

Modeled after PulseLite's 3× rolling-average rule, adapted for geospatial metrics:

1. **Same statistical family**: Z = (observed - mean(window)) / std(window). Interpretable, tuneable, no training data needed.
2. **Multi-metric**: Monitors `ndvi_delta`, `ndwi_delta`, `ndbi_delta`, and `area_delta` independently per preset.
3. **Alert taxonomy**: Automatically classifies alert type based on metric + direction (e.g., negative NDVI delta → `DEFORESTATION_SPIKE`).
4. **Bounded memory**: Rolling window of 10 observations per metric per preset — O(1) memory.

## Webhook Integration

When a threshold breach fires, `alert_dispatcher.py` makes real HTTP POSTs to configured Discord/Slack/custom webhook URLs with retry and exponential backoff (same approach as PulseLite's Discord alerts).

## Consequences

- **Positive**: Zero ML training, interpretable thresholds, real-time alerting.
- **Negative**: Window needs at least 3 observations before firing; cold-start means no alerts on first 2 queries.
