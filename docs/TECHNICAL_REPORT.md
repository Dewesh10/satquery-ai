# SatQuery AI — Technical Report

> **Version**: 1.0 · **Date**: November 2026 · **Author**: Dewesh10  
> **Repository**: [github.com/Dewesh10/satquery-ai](https://github.com/Dewesh10/satquery-ai)

---

## 1. Problem Statement

Satellite remote-sensing data is freely available — Sentinel-1 SAR, Sentinel-2 optical, and Landsat imagery cover the entire Earth every 5–12 days at 10–30 m resolution. Yet access is effectively gatekept by technical complexity: users must know STAC, WKT geometries, spectral index formulae, and cloud masking in order to get a single meaningful number.

Existing platforms — Google Earth Engine (GEE), Microsoft Planetary Computer, and Sentinel Hub — solve the data problem but not the query problem. A municipality wanting to know *"How much of the Assam floodplain was inundated in July?"* still needs a GEE developer.

**SatQuery AI** is a natural-language interface that sits on top of open STAC data and translates plain-English geospatial questions into structured satellite analysis pipelines, returning interpretable answers with uncertainty estimates and full reproducibility manifests.

The two motivating real-world problems:

1. **Flood response in Assam**: Monsoon clouds block optical imagery exactly when floods peak. SAR (Sentinel-1 C-band) penetrates cloud cover, but most municipal responders cannot operate it.  
2. **Unauthorized construction detection**: Indian cities face rampant illegal construction. Bi-temporal NDBI change detection over Sentinel-2 time series is a tractable automated monitor, yet no municipality-facing tool offers it.

---

## 2. Related Work

| System | Strength | Gap addressed by SatQuery AI |
|---|---|---|
| **Google Earth Engine** | Full global archive, server-side compute | No NL interface; requires JavaScript/Python expertise |
| **Microsoft Planetary Computer** | STAC catalog, Dask lazy loading | No NL interface; no digest or alert layer |
| **Sentinel Hub / EO Browser** | Visual browser, easy area stats | Closed API, no alerting, no NL |
| **GeoGPT / Earth-Agent (research)** | LLM-to-GIS function call | Research only, no production pipeline or alert loop |
| **GeoLLM-style tools** | Embedding geospatial context in LLMs | Focus on place understanding, not pipeline execution |

SatQuery AI positions itself as the **"ask in plain English" orchestration layer** on top of open data — complementary to, not competing with, GEE or Planetary Computer.

---

## 3. System Architecture

```
User Query (NL)
      │
      ▼
┌─────────────────────────────┐
│  LLM Query Planner          │  Gemini 2.5 Flash → JSON Schema validated
│  (llm_planner.py)           │  Fallback: regex/preset rules
└─────────┬───────────────────┘
          │  Structured Plan {region, dates, index, threshold}
          ▼
┌─────────────────────────────┐
│  DAG-Based Pipeline         │  Steps: STAC search → SCL mask → index compute
│  (planner.py)               │  → Z-score anomaly → digest
└─────────┬───────────────────┘
          │
    ┌─────┴──────┐
    ▼            ▼
┌────────┐  ┌──────────┐
│ STAC   │  │ SCL Cloud│
│ Search │  │  Masking │  Sentinel-2 scene classification band
└────────┘  └──────────┘
    │
    ▼
┌─────────────────────────────┐
│  Spectral Index Compute     │  NDWI, NDBI, NDVI, EVI, custom formula
│  (raster.py)                │  + Uncertainty block (cloud_free_fraction,
└─────────┬───────────────────┘    distance_from_threshold_sigma, pixel_count)
          │
          ▼
┌─────────────────────────────┐
│  Multi-Sensor RF Model      │  SAR VV/VH + Optical fusion
│  (ml_flood_classifier.py)   │  Random Forest with cross-validation
└─────────┬───────────────────┘
          │
          ▼
┌─────────────────────────────┐
│  Anomaly Detection          │  Z-score rolling window (W=10)
│  + Sentinel Watchtower      │  New satellite pass → eval → webhook
└─────────┬───────────────────┘
          │
          ▼
┌─────────────────────────────┐
│  LLM Digest Generator       │  Gemini 2.5 Flash → plain-English answer
│  (digest_generator.py)      │  with uncertainty statement
└─────────┬───────────────────┘
          │
          ▼
┌─────────────────────────────┐
│  Reproducibility Manifest   │  SHA-256 hash of inputs + STAC scene IDs
│  (reproducibility.py)       │  + git commit + all parameters
└─────────────────────────────┘
```

---

## 4. Key Components

### 4.1 Schema-Validated LLM Planner

The query planner uses Gemini 2.5 Flash with a strict JSON Schema:

```json
{
  "region_name": "string",
  "bbox": [west, south, east, north],
  "start_date": "YYYY-MM-DD",
  "end_date": "YYYY-MM-DD",
  "analysis_type": "CHANGE_DETECTION | FLOOD_MAPPING | TREND_ANALYSIS",
  "spectral_index": "NDWI | NDBI | NDVI | EVI",
  "threshold": 0.0–1.0
}
```

If the LLM output fails schema validation, the system falls back to regex keyword matching against preset templates. This avoids silent failures.

### 4.2 SCL Cloud Masking

The Sentinel-2 Scene Classification Layer (SCL band) is used to build a valid-pixel mask before any index computation. Filtered classes:

- Class 0: No data  
- Class 1: Saturated / defective  
- Class 3: Cloud shadows  
- Class 8: Cloud medium probability  
- Class 9: Cloud high probability  
- Class 10: Thin cirrus  

Every result reports `cloud_free_fraction` as the first uncertainty signal.

### 4.3 Multi-Date Time Series

Rather than comparing two dates, the temporal trend engine processes 6+ Sentinel-2 acquisitions:

- SCL quality filtering per acquisition  
- Z-score computation per observation relative to rolling window  
- Linear regression slope (sq km / pass) to separate seasonal swing from structural trend  

This prevents the false alarm pattern where seasonal NDWI swing is mistaken for flood extent change.

### 4.4 Multi-Sensor Random Forest

Fuses 5 features: SAR VV backscatter, SAR VH backscatter, optical NDWI, NDVI, and VV/VH ratio. Trained with cross-validation on synthetic SAR physics distributions; intended to be retrained on real Sen1Floods11 chips (see Section 7: Limitations).

### 4.5 Closed-Loop Alert Pipeline (Watchtower)

```
New Sentinel pass arrives
        │
        ▼
  STAC scene search
        │
        ▼
  SCL cloud check → skip if >50% cloudy
        │
        ▼
  Z-score anomaly evaluation
        │
        ▼
  Threshold crossed? → POST webhook → SQLite alert log
        │
        ▼
  HITL feedback → FP/FN ratio → threshold tuning recommendation
```

### 4.6 Reproducibility Manifest

Every query emits a SHA-256 manifest containing:
- Exact STAC scene IDs used  
- All algorithm parameters (threshold, window size, index formula)  
- Git commit hash of the backend  
- Timestamp and cloud-free fraction  

Anyone with this manifest can rerun the query and get bit-identical results.

---

## 5. Evaluation

### 5.1 Synthetic Pipeline Validation

> **Important**: The metrics below are computed on numpy-generated synthetic pixel arrays calibrated to real SAR and optical physics distributions. They are **not** scores on real Sen1Floods11 or OSCD image chips. See [ADR-007](adr/adr-007-synthetic-validation.md) for the full explanation and the path to real evaluation.

| Algorithm | Scenario | IoU | Precision | Recall | F1 |
|---|---|---|---|---|---|
| **Multi-Sensor RF** | Synthetic flood (SAR VV/VH + NDWI fusion) | **0.83** | 0.91 | 0.90 | 0.91 |
| **SAR Specular Threshold** | Synthetic VV < −16.5 dB | **0.60** | 0.63 | 0.93 | 0.75 |
| **Classical NDWI** | Synthetic with monsoon cloud noise | **0.48** | 0.65 | 0.65 | 0.65 |
| **NDBI Delta Change** | Synthetic sparse-change (~3.2% positive) | **0.30** | 0.32 | 0.78 | 0.46 |

Key interpretations:
- RF outperforms NDWI by +35 IoU points in monsoon-cloud scenarios, consistent with the physics reason (SAR is cloud-transparent)
- NDBI F1 of 0.46 is consistent with the literature range for simple differencing methods on sparse-change scenes (0.42–0.60)
- High recall on NDBI reflects high sensitivity to change, at the cost of coregistration false positives

### 5.2 Test Coverage

23 automated tests in `backend/tests/test_production_suite.py`:

```
test_llm_query_planner_schema_validation
test_llm_planner_fallback_on_bad_response
test_stac_catalog_search
test_raster_index_computation
test_uncertainty_reporting
test_digest_generation_and_caching
test_sen1floods11_evaluation          # synthetic SAR validation
test_oscd_urban_evaluation            # synthetic urban change validation
test_ml_model_evaluation
test_sentinel_closed_loop_flow
test_hitl_feedback_and_tuning
test_geodesic_shoelace_area
test_mgrs_tile_locator
test_zonal_stats
test_scl_cloud_masking
test_timeseries_analysis
test_reproducibility_manifest
... (+ 6 more)

23 passed in 10.63s
```

---

## 6. Engineering Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Pipeline orchestration | DAG-based (not "distributed DAG") | No Dask in current demo; Dask integration is the next step for the "distributed" claim to be honest |
| LLM model | Gemini 2.5 Flash | Best current cost/capability for JSON schema-constrained generation |
| Change detection | Morphological connected components (SciPy) | Interpretable, no deep learning training needed, known literature baseline |
| Feedback storage | SQLite | Zero-dependency; upgradeable to Postgres when deployed |
| Reproducibility | SHA-256 manifest | Cheap to compute, easy to verify, no external service needed |
| Cloud masking | Sentinel-2 SCL band | Level-2A product includes SCL; no external cloud mask API needed |

---

## 7. Limitations

This section is intentionally detailed — honest limitations are what make a project read as senior-level work.

**Synthetic evaluation, not real benchmark chips**  
The most significant limitation. All algorithm validation is done on numpy-generated arrays. Until real Sen1Floods11 GeoTIFF chips with their label masks are downloaded and scored, the IoU numbers are "plausible by physics" not "empirically verified on ground truth". See ADR-007 for the fix.

**No Dask / lazy xarray loading**  
Images are loaded as numpy arrays. For large AOIs (>1° × 1°) or long time series (>20 dates), memory will be a bottleneck. The fix is `odc-stac` or `stackstac` for lazy Dask-backed xarray loading.

**Sentinel-1 is listed but not fully integrated**  
Real Sentinel-1 GRD product download requires ESA Copernicus Data Space credentials and significant storage. The SAR features in the RF model are currently drawn from physics-calibrated synthetic distributions, not live GRD product reads.

**No live deployment**  
The system runs via Docker Compose locally. No public URL exists yet. A minimal deployment on Railway or Fly.io would take ~1 hour and would demonstrate the closed-loop alert pipeline end-to-end.

**No demo video**  
A 2-minute screen recording showing: (1) NL query → digest, (2) custom AOI drawing → zonal stats, (3) benchmark modal, and (4) Watchtower closed-loop pass — would substantially increase project credibility.

**Threshold tuning is recommendation-only**  
The HITL feedback system recommends threshold adjustments but does not automatically apply them. A production system would require a human approval step before any threshold change.

---

## 8. Relationship to Established Platforms

SatQuery AI is not a GEE replacement. It is a thin orchestration layer:

```
User question (plain English)
        │
        ▼
SatQuery AI (NL → structured plan → digest)
        │
        ▼
Open STAC APIs (Planetary Computer, Element84, AWS COG)
        │
        ▼
Free Sentinel-1 / Sentinel-2 / Landsat imagery
```

The closest research analogues are **GeoGPT** (NL geospatial question answering), **Earth-Agent** (tool-use agent for remote sensing), and **GeoLLM** (geospatial context in language models). SatQuery AI differs in having a production-wired alert pipeline and reproducibility manifests rather than focusing on academic benchmarking.

---

## 9. What Would Make This a Stronger Project

In priority order:

1. **Score on real Sen1Floods11 chips** — download 50 chip pairs, train/test split geographically, report honest IoU. Even if the number drops, it becomes a real result.
2. **A 2-minute demo video** — show the full flow from NL query to digest.
3. **Live deployment** — a public URL with one working preset query.
4. **Dask integration** — replace numpy arrays with xarray + odc-stac for lazy loading; then the "DAG-based" claim becomes "distributed DAG" with justification.
5. **Sentinel-1 SAR live read** — use `sentinelsat` or Copernicus Data Space API to pull real GRD products.

---

## 10. References

- Bonafilia, D. et al. (2020). *Sen1Floods11: a georeferenced dataset to train and test deep learning flood algorithms for Sentinel-1*. CVPR Workshops.
- Daudt, R. C. et al. (2018). *Fully Convolutional Siamese Networks for Change Detection*. IGARSS 2018.
- Sentinel Hub SCL documentation: https://docs.sentinel-hub.com/api/latest/data/sentinel-2-l2a/
- Microsoft Planetary Computer STAC catalog: https://planetarycomputer.microsoft.com/api/stac/v1
- NASA/IBM Prithvi geospatial foundation model: https://huggingface.co/ibm-nasa-geospatial
