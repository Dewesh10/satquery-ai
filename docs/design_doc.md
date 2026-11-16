# SatQuery AI — Design Document

## Problem Statement

Government land-use decision-makers (Tehsildars, municipal GIS analysts, disaster response coordinators) currently need expensive desktop GIS software (ArcGIS/QGIS) and months of training to process satellite imagery. Multi-gigabyte scene downloads, manual NDVI computation, and bespoke change map generation take days per analysis.

**How might we let a district collector simply ask in plain English: "Has there been unauthorized construction in Sector 4 of my district?" and get an actionable response in seconds?**

## Solution

SatQuery AI provides:
1. A natural-language query copilot that translates plain-text questions into executable DAG pipelines
2. A NumPy spectral math engine computing NDVI/NDWI/NDBI change indices from STAC-registered COG assets
3. A rolling Z-score anomaly detector that fires real webhook alerts when thresholds are breached
4. An AI narrative digest (Gemini-backed or rule-based) explaining results in administrative language
5. Export pipelines for official government report formats

## What Is Real vs. Simulated

| Component | Status | Notes |
|---|---|---|
| OSM Nominatim geocoding | ✅ REAL | Live HTTP call |
| Earth Search STAC queries | ✅ REAL | Live HTTP call |
| NumPy band math (NDVI/NDWI) | ✅ REAL | Real formulas on pixel arrays |
| Z-score anomaly detector | ✅ REAL | Real rolling baseline logic |
| Webhook dispatch (retry) | ✅ REAL | Real HTTP POST |
| SQLite query history | ✅ REAL | Real persistence |
| AI Digest (Gemini) | ✅ REAL (if key set) | Free tier |
| Raster pixel arrays | ⚠️ SIMULATED | np.random — no real scene download |
| Vision model outputs | ⚠️ SIMULATED | Weights not integrated |
| Multilingual summaries | ⚠️ TEMPLATED | Static templates, not NMT |
