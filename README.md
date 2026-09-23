# SATQUERY AI — Earth-Observation AI Copilot

**SATQUERY AI** is an open-source Earth-observation copilot prototype where users ask natural-language questions about satellite imagery (Sentinel-2, Landsat-8/9, Sentinel-1 SAR) and receive map-grounded, evidence-backed answers.

---

## 🛰 Core Capabilities

- **3D Globe / Vector Map Workspace**: Geospatial tile rendering with AOI drawing tools (polygons & bounding boxes), spectral layer controls (Optical RGB, False Color Infrared, NDVI, NDWI, SAR Radar), and coordinate readout.
- **Natural-Language Query Planner**: Compiles prompts like *"Show built-up expansion in Dubai between March 2018 and February 2024"* into structured DAG execution graphs with step-by-step transparency. Respects explicit `preset_id` parameters passed in request payloads.
- **Computer Vision Output Placeholders**: Simulated bi-temporal change detection, land cover segmentation, vessel detection, and vector polygon extraction formats (`SIMULATED — Model Integration Pending`).
- **Templated Multilingual Evidence Summaries**: Generates evidence summaries in English, Hindi, and Assamese citing Scene IDs, timestamps, coordinates, sensor modality, and bounding boxes (`TEMPLATED_SUMMARY`).
- **Interactive Spatial Links**: Clicking any evidence citation card flies the 3D map directly to that spatial chip footprint.
- **Before/After Split Screen**: Bi-temporal swipe slider to compare pre vs post satellite scenes side-by-side.
- **Timeline Time Slider**: Historical temporal scrubber with automated time-series playback.
- **Multi-Format Exporter**: Export GeoJSON change vectors, CSV metric summary tables, provisional screening logs, STAC GeoTIFF metadata manifests, or executive PDF reports.
- **Sentinel Orbit Watchtower**: Simulated satellite pass alert trigger engine with emergency webhook dispatching.

---

## ⚠️ Current Limitations

1. **Simulated vs. Real Data**: Raster pixel array inputs use simulated NumPy distributions (`np.random.uniform`), and the $n=32$ scene baseline uses demo distributions (`SIMULATED_BASELINE`). Live COG byte-range pixel extraction pipelines are spec'd in `extract_stac_pixels.py` but pending live production wiring.
2. **Computer Vision & LLM Engines**: CV outputs (change detection, segmentation, object detection) and VLM summaries return simulated/templated JSON structures. Pretrained PyTorch/TensorFlow deep learning weights and live LLM inference calls are not currently integrated.
3. **Illustrative Validation Benchmarks**: Validation targets (e.g. Assam CWC flood bulletin targets) are illustrative benchmark references (`illustrative_validation_target`) rather than claims of certified ground-truth agreement.
4. **No Authentication**: All REST API endpoints are currently unauthenticated. Production deployment requires API keys, Role-Based Access Control (RBAC), and audit logging.
5. **Simulated Watchtower Alerts**: Sentinel Watchtower orbit pass breaches are manually triggered via the `/api/sentinel/alerts/trigger` simulation endpoint rather than listening to live STAC catalog feeds.
6. **Frontend Bundle Size**: Main JS chunk size is ~809KB (code-splitting pending).

---

## 📂 Project Structure

```
satquery-ai/
├── backend/
│   ├── app/
│   │   ├── main.py               # FastAPI application & endpoints
│   │   ├── core/
│   │   │   ├── config.py         # Preset benchmark scenarios
│   │   │   └── data_store.py     # STAC satellite dataset store
│   │   └── services/
│   │       ├── planner.py        # NL Query Planner (DAG compiler)
│   │       ├── catalog.py        # STAC catalog query service
│   │       ├── raster.py         # Raster processing & GeoJSON engine (Simulated Data)
│   │       ├── vision.py         # Simulated CV output service
│   │       ├── vlm_evidence.py   # Templated Multilingual Evidence Summaries
│   │       ├── sentinel_monitor.py # Sentinel Watchtower alert & webhook engine
│   │       ├── replay.py         # Timeline replay & execution store
│   │       └── export.py         # GeoJSON, CSV, PDF, STAC Manifest exporter
│   ├── scripts/
│   │   ├── test_all_endpoints.py # End-to-end API audit test suite
│   │   └── compute_historical_baseline_n30.py # Baseline computation script
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx               # SatQuery Copilot Workspace
│   │   ├── components/           # Navbar, Map, Copilot, Evidence, Studios
│   │   ├── lib/api.ts            # API client with demo fallback
│   │   └── types/                # TypeScript interface definitions
│   └── package.json
└── README.md
```

---

## ⚡ Quickstart

### 1. Launch Python FastAPI Backend
```powershell
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```
*Backend runs on `http://127.0.0.1:8000`.*

### 2. Launch React Frontend
```powershell
cd frontend
npm install
npm run dev
```
*Frontend opens on `http://localhost:3000`.*

---

## 🌍 Benchmark Demo Scenarios Included

1. **Dubai Built-Up Growth (2018 vs 2024)** — Optical Sentinel-2 (+42.8 sq km growth).
2. **Amazon Deforestation (2020 vs 2024)** — Landsat-8/9 NDVI canopy loss (-68.5 sq km clearing).
3. **Lake Mead Drought & Water Loss (2015 vs 2023)** — Sentinel-2 NDWI surface retreat (-31.2 sq km shrinkage).
4. **Assam Brahmaputra Flood Inundation** — Sentinel-1 SAR Radar specular reflection drop (+114.6 sq km submerged).
5. **Singapore Port Maritime Traffic** — Capella SAR Spotlight high-resolution ship detection (148 vessels).
