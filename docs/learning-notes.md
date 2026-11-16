# Learning Notes — What Actually Broke

An honest engineering log of what went wrong during SatQuery AI development.

## Planner Preset Override Bug

The original `planner.py` ran OSM geocoding and keyword matching *before* checking `user_preset_id`. A prompt containing "built-up" matched the keyword `"up"`, resolving to `india_up` instead of `dubai_urban` even when `preset_id: "dubai_urban"` was explicitly in the request body. Fix: moved `user_preset_id` check to Priority 0, added regex word boundaries (`\b`).

## Vite Bundle Size

Initial `npm run build` produced an 809.41 kB main chunk — a single warning-flagged bundle containing Leaflet, Recharts, and all Lucide icons. Added `manualChunks` in `vite.config.ts` and `React.lazy()` dynamic imports for each Studio tab. Main chunk dropped to 79.4 kB.

## API Key Middleware Order

FastAPI processes middlewares in reverse registration order (LIFO). The API key auth middleware must be registered *before* the rate limiter so auth runs first (registered second = executes first). Easy to get backwards.

## SQLite WAL Mode

SQLite default journal mode causes `database is locked` errors under concurrent reads in the test suite. Solution: open with `check_same_thread=False` and use short-lived `with sqlite3.connect(DB_PATH) as conn:` context managers (auto-commit).

## Anomaly Detector Cold Start

The Z-score anomaly detector needs at least 3 observations in its rolling window before it can fire. On a fresh deployment, the first 2 queries won't trigger alerts. This is by design — not a bug.
