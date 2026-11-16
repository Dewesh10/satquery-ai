# ADR-002 — Spectral Analysis: NumPy Classical Statistics over Deep Learning

**Date**: 2024-11-05  
**Status**: Accepted

## Context

Change detection can be done via:
- **Classical statistics**: NDVI/NDWI delta + Z-score threshold
- **Deep learning**: Siamese U-Net, ChangeFormer, YOLO-World

## Decision

Use **NumPy vectorized spectral index math + Z-score rolling anomaly detection** for the live query pipeline.

## Rationale

1. **Zero-latency**: NumPy on a CPU array completes in <50ms. A U-Net forward pass requires GPU or minutes on CPU.
2. **Mathematically auditable**: Every NDVI = (NIR - Red) / (NIR + Red) calculation can be explained to a district collector. Neural network decisions cannot.
3. **No GPU dependency**: Prototype can run on a $5/month VPS. Deep learning requires expensive GPU instances.
4. **Statistically honest**: Z-score threshold is a well-understood statistical method with interpretable thresholds (2.5σ, 3.0σ).

## Deep Learning Role

Neural model weights (Siamese U-Net, SpaceNet-7, LEVIR-CD) are specified as the **offline GPU batch ingestion tier** for high-resolution target verification. They are explicitly labeled `SIMULATED — integration pending` in the codebase.

## Consequences

- **Positive**: Instant query responses, mathematical transparency, no GPU cost.
- **Negative**: Classical methods can't segment individual building outlines or detect subtle camouflaged changes.
