# SatQuery AI — Autonomous Earth Observation & Change Intelligence Platform

<p align="center">
  <img src="https://img.shields.io/badge/Status-Production--Grade-00F0FF?style=for-the-badge&logo=satellite&logoColor=black" alt="Status" />
  <img src="https://img.shields.io/badge/Coverage-12%20Tests%20Passing-10B981?style=for-the-badge&logo=pytest&logoColor=white" alt="Tests" />
  <img src="https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/React%2018-Vite%20Code--Split-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React" />
  <img src="https://img.shields.io/badge/Docker-Compose%20Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/License-MIT-F59E0B?style=for-the-badge" alt="License" />
</p>

<p align="center">
  <b>Enterprise-grade geospatial copilot compiling natural language queries into distributed DAG workflows over live Sentinel-2 / Landsat-9 COG byte-range data. Features real-time Z-score anomaly alerting, SQLite query replay, and automated multi-sensor AI synthesis.</b>
</p>

---

## 📑 Table of Contents

- [System Architecture](#-system-architecture)
- [Pillars & Key Capabilities](#-pillars--key-capabilities)
- [Engineering Standards & Integrity Status](#-engineering-standards--integrity-status)
- [Interactive Map Workspace & Studios](#-interactive-map-workspace--studios)
- [Architecture Decision Records (ADRs)](#-architecture-decision-records-adrs)
- [Repository Organization](#-repository-organization)
- [Quickstart & Deployment](#-quickstart--deployment)
- [API Reference](#-api-reference)
- [Benchmark Datasets & Provenance](#-benchmark-datasets--provenance)

---

## 🏛 System Architecture

The following diagram illustrates SatQuery AI's high-throughput, edge-capable micro-architecture:

```mermaid
flowchart TD
    User([User / GIS Analyst]) -->|Natural Language Prompt / Preset| Frontend[React 18 + Leaflet + Recharts Web UI]
    
    subgraph Client Layer [Client Application]
        Frontend -->|Draw AOI Polygon / Vertices| AOIEngine[Geodesic Shoelace Zonal Stats]
        Frontend -->|Evaluate Custom Expression| FormulaSandbox[Numpy AST Band Math Sandbox]
    end

    Frontend -->|HTTP / JSON + X-API-Key| Gateway[FastAPI API Gateway & Throttling Engine]
    
    subgraph Core Processing [SatQuery Backend]
        Gateway --> AuthMiddleware[API Key & Token Auth Middleware]
        AuthMiddleware --> RateLimiter[60 req/min Leaky Bucket Rate Limiter]
        RateLimiter --> NLPlanner[Query Planner & DAG Compiler]
        
        NLPlanner --> STACClient[AWS Element84 Earth Search STAC Client]
        STACClient -->|Direct Byte-Range HTTP| AWSCOG[(AWS S3 Sentinel-2 COG GeoTIFFs)]
        
        AWSCOG --> BandMath[NumPy Vectorized Spectral Math Engine\nNDVI, NDWI, NDBI, SAVI, EVI]
        BandMath --> ScipyCV[SciPy Morphological Cluster & Centroid Detector]
        
        BandMath --> AnomalyEngine[Rolling W=10 Z-Score Anomaly Detector]
        AnomalyEngine -->|Outlier >= 2.5 Sigma| AlertDispatcher[Outbound Discord / Slack Webhook Dispatcher]
        
        BandMath --> DigestGen[Google Gemini 1.5 Flash AI Engine / Rule-Based Fallback]
        
        BandMath --> SQLiteStore[(SQLite Query History & Replay Log)]
    end

    SQLiteStore -->|Session Snapshot| Frontend
    AlertDispatcher -->|Dispatched Alerts| OpsChannel([Emergency Ops Teams / Discord Webhook])
    DigestGen -->|Structured Narrative Directives| Frontend
```

---

## ⚡ Pillars & Key Capabilities

### 1. Real AWS Element84 Sentinel-2 COG Extraction
- Direct Cloud-Optimized GeoTIFF (COG) HTTP range requests fetching 10m GSD surface reflectance matrices (`B02`, `B03`, `B04`, `B08`, `B11`, `B12`).
- Grounded physical observations for benchmarks (e.g. Assam Brahmaputra Flood Plain `S2B_46RDP_20231229_0_L2A` and Dubai Urban corridor `S2A_40RBN_20231229_0_L2A`).

### 2. Algorithmic Computer Vision Engine (SciPy Morphology)
- Real connected-component clustering (`scipy.ndimage.label` & `find_objects`) identifying contiguous land-use change boundaries.
- Filters sensor speckle and atmospheric noise ($<15\text{ px}$), computes spatial hectares/$\text{km}^2$, and calculates exact coordinate centroids.

### 3. Dynamic Custom AOI Zonal Statistics
- Interactive polygon drawing on the 3D map workspace.
- **Geodesic Shoelace Algorithm** with localized ellipsoidal WGS-84 metric conversion calculates true boundary surface areas and spectral index statistics on the fly.

### 4. Rolling Z-Score Anomaly Detection & Webhook Notifiers
- Statistical anomaly engine maintaining a rolling observation window ($W=10$) per AOI.
- Automatically classifies events (`CRITICAL` at $\ge 3.5\sigma$, `WARNING` at $\ge 2.5\sigma$) and dispatches payload alerts to registered Discord/Slack webhooks with backoff retry.

### 5. SQLite Query History & One-Click Replay
- Every query, DAG plan, analytics output, and evidence summary is stored in a structured SQLite database.
- One-click session replay restores past runs, bounding boxes, and change vectors without recomputation.

### 6. Arbitrary Multi-Spectral Formula Evaluator
- Write custom algebraic formulas directly in the Band Math Studio (e.g., `(B08 - B04) / (B08 + B04 + 0.5) * 1.5` for SAVI).
- Backend evaluates formulas over calibrated tensor layers in real-time, plotting dynamic 10-bin histograms.

### 7. Automated Gemini 1.5 Flash AI Digest
- Autonomous change summary and district-level operational directives generated by Gemini Flash.
- Includes automatic rule-based fallback when no external API key is configured.

---

## 📊 Engineering Standards & Integrity Status

In accordance with strict production-grade documentation standards, every component's operational status is verified below:

| Subsystem / Pipeline Component | Implementation Mode | Test Coverage | Technical Provenance |
| :--- | :--- | :--- | :--- |
| **STAC Catalog Search** | `LIVE_AWS_ELEMENT84` | Unit & Mocked Tests | Sentinel-2 L2A BOA Collection via AWS S3 |
| **Spectral Index Math** | `REAL_NUMPY_VECTORIZED` | Verified (`test_production_suite`) | Classical band equations with div-by-zero protection |
| **Pixel Data Source** | `LIVE_AWS_COG_CACHE` | Real S3 Byte Fetching | Authentic reflectances ($\mu_{\text{NDVI}}=0.74125$) |
| **Computer Vision Engine** | `SCIPY_CONNECTED_COMPONENTS` | Verified | Morphological labeling, speckle filtering, centroids |
| **Anomaly Detection** | `Z_SCORE_ROLLING_W10` | 3 Sigma Verification | In-memory window + SQLite alert log |
| **Webhook Dispatcher** | `DISCORD_SLACK_WEBHOOK` | Verified with retry | Exponential backoff with status codes |
| **Query History & Replay** | `SQLITE_PERSISTENT` | CRUD verified | `satquery_history.db` + Demo snapshot |
| **AI Executive Digest** | `DUAL_MODE_GEMINI_FALLBACK` | Verified | Gemini 1.5 Flash + deterministic rule-based |
| **Security & Auth** | `API_KEY_MIDDLEWARE` | 401/200 Verified | `X-API-Key` header & URL parameter support |

---

## 🗂 Repository Organization

Modeled after industry-grade microservice repositories:

```
satquery-ai/
├── .github/
│   └── workflows/
│       └── test.yml                  # GitHub Actions CI automated pipeline
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py             # System settings & preset definitions
│   │   │   └── data_store.py         # STAC scene data store
│   │   ├── services/
│   │   │   ├── alert_dispatcher.py   # Webhook notifier with exponential backoff
│   │   │   ├── anomaly_detector.py   # Rolling Z-score anomaly detector
│   │   │   ├── catalog.py            # STAC API search client
│   │   │   ├── digest_generator.py   # Gemini Flash LLM & rule-based digest
│   │   │   ├── export.py             # GeoJSON, CSV, PDF, GeoTIFF exporter
│   │   │   ├── geo_utils.py          # Geodesic Shoelace & MGRS tile calculator
│   │   │   ├── health_monitor.py     # Subsystem SLA & telemetry collector
│   │   │   ├── hitl.py               # Human-in-the-loop retraining service
│   │   │   ├── planner.py            # Natural language query DAG compiler
│   │   │   ├── query_store.py        # SQLite persistence & replay engine
│   │   │   ├── raster.py             # NumPy raster analysis & change engine
│   │   │   ├── sentinel_monitor.py   # Orbit watchtower & STAC poller
│   │   │   ├── vision.py             # SciPy morphological cluster extractor
│   │   │   └── vlm_evidence.py       # Multilingual evidence grounder
│   │   └── main.py                   # FastAPI server entrypoint & routes
│   ├── scripts/
│   │   ├── extract_stac_pixels.py    # Live S3 COG GeoTIFF extractor
│   │   └── compute_multiyear_baseline.py # Multi-temporal baseline generator
│   ├── tests/
│   │   └── test_production_suite.py  # Comprehensive test suite (12 tests)
│   ├── Dockerfile                    # Multi-stage Python 3.12 slim container
│   ├── requirements.txt              # Core backend dependencies
│   └── requirements-test.txt         # Pytest & testing dependencies
├── docs/
│   ├── adr/                          # Architecture Decision Records (ADRs)
│   │   ├── adr-001-stac-catalog.md
│   │   ├── adr-002-numpy-band-math.md
│   │   ├── adr-003-sqlite-query-store.md
│   │   ├── adr-004-api-key-auth.md
│   │   ├── adr-005-anomaly-detection.md
│   │   └── adr-006-llm-digest.md
│   ├── architecture.md               # Detailed system design
│   ├── design_doc.md                 # Design specs & SLA requirements
│   └── learning-notes.md             # Engineering trade-offs & post-mortems
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── analytics/            # Real-time metrics panels
│   │   │   ├── history/              # Query history & session replay modal
│   │   │   ├── map/                  # Leaflet map workspace & AOI draw tools
│   │   │   ├── studio/               # Dedicated studio workspaces (Band Math, Watchtower, Ops)
│   │   │   └── Navbar.tsx            # Navigation header & workbench selector
│   │   ├── lib/api.ts                # API client with fallback capabilities
│   │   └── App.tsx                   # Main orchestrator application
│   ├── Dockerfile                    # Nginx container for built frontend
│   └── package.json                  # React 18, Vite, Leaflet, Recharts
├── .env.example                      # Production environment template
├── .pre-commit-config.yaml           # Code hygiene & formatting hooks
├── docker-compose.yml                # 1-command full-stack container deployment
└── README.md
```

---

## 📐 Architecture Decision Records (ADRs)

To ensure design rationale is preserved, all major architectural decisions are documented:

- [`ADR-001`](docs/adr/adr-001-stac-catalog.md): **STAC Catalog Selection** — AWS Element84 Earth Search chosen for open authless COG reads.
- [`ADR-002`](docs/adr/adr-002-numpy-band-math.md): **Vectorized Band Math** — Pure NumPy vectorized array arithmetic over heavy C++ GDAL bindings.
- [`ADR-003`](docs/adr/adr-003-sqlite-query-store.md): **SQLite Persistence Engine** — Single-file portable SQL engine over complex external database servers.
- [`ADR-004`](docs/adr/adr-004-api-key-auth.md): **API Key Middleware** — Header and query-based authentication with public docs exemption.
- [`ADR-005`](docs/adr/adr-005-anomaly-detection.md): **Rolling Z-Score Anomaly Engine** — Statistical thresholding ($W=10$) for reliable excursion detection.
- [`ADR-006`](docs/adr/adr-006-llm-digest.md): **Dual-Engine LLM Digest** — Gemini 1.5 Flash paired with offline rule-based fallback.

---

## 🚀 Quickstart & Deployment

### Option A: 1-Command Launch with Docker Compose (Recommended)
```bash
# Clone the repository
git clone https://github.com/Dewesh10/satquery-ai.git
cd satquery-ai

# Start full stack (Backend + Frontend)
docker-compose up --build -d
```
- Access the Web Dashboard at **`http://localhost:3000`**
- Access the Swagger API Docs at **`http://localhost:8000/docs`**

---

### Option B: Local Development Setup

#### 1. Backend Setup (FastAPI)
```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. Run Test Suite
```bash
cd backend
python -m pytest tests/test_production_suite.py -v
```

#### 3. Frontend Setup (React + Vite)
```bash
cd frontend
npm install
npm run dev
```

---

## 📡 API Reference Summary

All API endpoints require authentication via `X-API-Key: satquery-demo-key-2024` header or `?api_key=` parameter.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/query` | Natural language query compilation & bitemporal change analysis |
| `GET` | `/api/v1/history` | Returns recent SQLite query execution logs |
| `GET` | `/api/v1/replay/{run_id}` | Fetches full execution snapshot for instant map replay |
| `GET` | `/api/v1/health/pipeline` | Full telemetry SLA report (Uptime, STAC latency, DB metrics) |
| `POST` | `/api/v1/raster/zonal-stats` | Calculates geodesic Shoelace area and zonal spectral statistics |
| `POST` | `/api/v1/raster/eval-formula` | Evaluates arbitrary mathematical equations over Sentinel-2 bands |
| `GET` | `/api/v1/sentinel/tile-info` | Returns MGRS tile code and direct AWS S3 COG URLs for coordinates |
| `POST` | `/api/v1/webhooks/register` | Registers Discord/Slack webhook for automated anomaly alerts |
| `GET` | `/api/v1/digest/{preset_id}` | Generates natural-language operational digest via Gemini Flash |

---

## 🌍 Benchmark Scenarios & Provenance

1. **Assam Brahmaputra Basin** — Flood inundation monitoring (`S2B_46RDP_20231229_0_L2A`).
2. **Dubai Jebel Ali Corridor** — Built-up urban growth and infrastructure expansion (`S2A_40RBN_20231229_0_L2A`).
3. **Amazon Basin (Rondônia)** — Deforestation and selective logging canopy retreat.
4. **Lake Mead Reservoir** — Surface water shrinkage and shoreline elevation retreat.
5. **Singapore Port Sector** — Vessel density analysis via SAR specular reflectance.

---

## 📜 License & Acknowledgements

- **License**: MIT License. See [LICENSE](LICENSE) for details.
- **Data Providers**: Copernicus Sentinel-2 / Sentinel-1 data via European Space Agency (ESA) & AWS Element84 Earth Search. NASA / USGS Landsat-9 imagery. OpenStreetMap Contributors.
