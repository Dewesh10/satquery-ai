# ADR-007 — Synthetic Pipeline Validation Instead of Real Benchmark Chips

**Status**: Accepted  
**Date**: 2026-11-19  
**Deciders**: Project maintainer  
**Tags**: benchmarking, integrity, evaluation, datasets

---

## Context

SatQuery AI includes an evaluation module (`eval_benchmarks.py`) that tests three algorithms:

1. **Multi-Sensor Random Forest** — SAR (VV/VH) + Optical (NDWI) fusion for flood mapping  
2. **SAR Specular Thresholding** — VV backscatter threshold (< −16.5 dB) for flood detection  
3. **NDBI Delta Change Detection** — Normalized Difference Built-up Index differencing for urban expansion  

An earlier version of the codebase labelled these evaluation results as "Sen1Floods11 results" and "OSCD results". A code review identified that the evaluation used `numpy`-generated synthetic pixel arrays — not real GeoTIFF image chips from those datasets. Using those dataset names for synthetic results is dishonest labelling.

---

## Decision

Replace all references to "Sen1Floods11 benchmark" and "OSCD benchmark" with **"Synthetic Pipeline Validation"** everywhere they appear: backend service, frontend modal, README, API endpoint descriptions, and status table.

The evaluation module retains backward-compatible function aliases for test continuity, but adds:
- An `evaluation_type: SYNTHETIC_PIPELINE_VALIDATION` field in every result dict  
- A module-level docstring explaining the synthetic nature  
- Clear `[!IMPORTANT]` boxes in the README  
- An amber warning banner in the frontend `ModelBenchmarkingModal`

---

## What the Synthetic Evaluation Does (and Does Not) Prove

### It **does** prove:
- The Random Forest model learns meaningful decision boundaries (synthetic SAR scores clearly above NDWI baseline)  
- The morphological connected-component engine correctly labels sparse-change arrays (~3.2% positive pixels)  
- The relative ordering of algorithms is consistent with physical intuition  
- The pipeline runs end-to-end without errors  

### It **does not** prove:
- Absolute metric values match what the algorithms would score on real Sen1Floods11 or OSCD chips  
- Generalization to real geographic domains, acquisition geometries, or atmospheric conditions  
- That the numbers can be cited as "Sen1Floods11 results" or "OSCD results"

---

## Why Synthetic Arrays (for now)

| Reason | Detail |
|---|---|
| No live SAR API in demo tier | Real Sentinel-1 GRD download requires ESA Copernicus Data Space credentials and 400–800 MB downloads per scene |
| Sen1Floods11 is 11 GB | Full dataset requires `gsutil` or gcloud auth; not viable in a CI/CD pipeline without cloud storage budget |
| OSCD requires IEEE DataPort registration | Free, but manual; not automated |
| Goal is algorithm correctness, not leaderboard position | The relative RF vs NDWI comparison is what matters architecturally |

---

## Path to Real Benchmark Evaluation

### Sen1Floods11

```bash
# Install gsutil (Google Cloud SDK)
gsutil -m cp -r gs://sen1floods11_dataset/v1.1/data/flood_events/HandLabeled/ ./data/sen1floods11/

# Geographic split CSVs
gsutil cp gs://sen1floods11_dataset/v1.1/splits/flood_handlabeled_*.csv ./data/sen1floods11/
```

Replace `eval_benchmarks.py:evaluate_sar_threshold_synthetic()` with a function that:
1. Loads GeoTIFF chip pairs (Sentinel-1 + Sentinel-2 co-registered) using `rasterio`
2. Loads label masks (binary flood / non-flood)
3. Trains on `flood_handlabeled_train.csv` splits, tests on `flood_handlabeled_test.csv`
4. Reports IoU, Precision, Recall, F1 from real pixel predictions

Add to `requirements.txt`:
```
rasterio>=1.3.9
geopandas>=0.14.0
```

### OSCD

Download from IEEE DataPort: https://ieee-dataport.org/open-access/oscd-onera-satellite-change-detection

Replace `evaluate_urban_change_detection_synthetic()` with a chip loader, then compare `im1`/`im2` pairs against `cm.png` label masks.

---

## Consequences

**Positive**:
- No reviewer can accuse the project of falsely claiming dataset scores  
- The honest framing ("pipeline validation") is what a senior engineer would say  
- The path to real evaluation is fully documented  

**Negative**:
- Numbers look less impressive without real benchmark labels  
- Until real chips are added, the evaluation section carries a caveat  

---

## Related ADRs

- [ADR-005](adr-005-raster-pipeline.md) — Raster pipeline design
- [ADR-006](adr-006-llm-digest.md) — LLM digest with schema validation
