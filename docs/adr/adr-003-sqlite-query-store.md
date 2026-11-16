# ADR-003 — Persistence: SQLite over PostgreSQL

**Date**: 2024-11-05  
**Status**: Accepted

## Context

SatQuery AI needs persistent storage for query history, alert logs, and replay snapshots.

## Decision

Use **SQLite** (Python stdlib `sqlite3`) with two tables: `query_history` and `alert_log`.

## Rationale

1. **Zero additional dependency**: `sqlite3` is in Python stdlib. PostgreSQL requires `psycopg2`, a running DB server, and connection pool management.
2. **Single-file portability**: The `.db` file can be copied, backed up, or committed for demo snapshots — same philosophy as PulseLite's CSV persistence.
3. **Prototype-appropriate**: SatQuery AI is a prototype. SQLite handles thousands of queries per day trivially. PostgreSQL's scalability is unnecessary at this stage.
4. **Docker volume**: The SQLite file is mounted as a Docker volume (`satquery_db`), surviving container restarts.

## Migration Path

Moving to PostgreSQL later is a ~50-line change: replace `sqlite3` calls with `psycopg2`, adjust connection strings. The table schemas are identical.

## Consequences

- **Positive**: Zero setup, works immediately, portable.
- **Negative**: No concurrent write scaling (not needed), no built-in replication.
