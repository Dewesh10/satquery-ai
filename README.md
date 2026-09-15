# SATQUERY AI — Earth-Observation AI Copilot

**SATQUERY AI** is an Earth-observation copilot where users ask natural-language questions about satellite imagery (Sentinel-2, Landsat-8/9, Capella SAR) and receive map-grounded, evidence-backed answers.

---

## 🛰 Core Capabilities

- **3D Globe / Vector Map Workspace**: Full geospatial tile rendering with AOI drawing tools (polygons & bounding boxes), spectral layer controls (Optical RGB, False Color Infrared, NDVI, NDWI, SAR Radar), and coordinate readout.
- **Natural-Language Query Planner**: Compiles prompts like *"Show built-up expansion in Dubai between March 2018 and February 2024"* into structured DAG execution graphs with step-by-step transparency.
- **Bi-Temporal Computer Vision Engine**: Automated change detection, land cover segmentation, vessel detection, and vector polygon extraction.
- **Vision-Language Evidence Grounding**: Synthesizes findings with mandatory evidence cards citing exact Scene IDs, timestamps, coordinates, sensor modality, and bounding boxes.
- **Interactive Spatial Links**: Clicking any evidence citation card smoothly flies the 3D map directly to that exact spatial chip footprint.
- **Before/After Split Screen**: Bi-temporal swipe slider to compare pre vs post satellite scenes side-by-side.
- **Timeline Time Slider**: Historical temporal scrubber with automated time-series playback.
- **Multi-Format Exporter**: Export GeoJSON change vectors, CSV metric summary tables, or executive PDF reports.
- **Zero-Latency Demo Resiliency**: Shipped with pre-loaded curated datasets for 5 benchmark scenarios (Dubai, Amazon, Lake Mead, Assam, Singapore Port).

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
│   │       ├── raster.py         # Raster processing & GeoJSON engine
│   │       ├── vision.py         # CV models (Change, Seg, Detections)
│   │       ├── vlm_evidence.py   # Grounded VLM evidence generator
│   │       ├── replay.py         # Timeline replay & execution store
│   │       └── export.py         # GeoJSON, CSV, PDF report exporter
│   ├── requirements.txt
│   └── run.py                    # Backend server entrypoint
├── frontend/
│   ├── src/
│   │   ├── App.tsx               # SatQuery Copilot Workspace
│   │   ├── components/           # Navbar, Map, Copilot, Evidence, Analytics
│   │   ├── lib/api.ts            # API client with offline demo fallback
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
python run.py
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
