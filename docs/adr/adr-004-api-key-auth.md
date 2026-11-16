# ADR-004 — Authentication: Static API Key over OAuth2

**Date**: 2024-11-05  
**Status**: Accepted

## Context

The API needs protection against unauthenticated access.

## Decision

Use a **static `X-API-Key` header or `api_key` query parameter**, configurable via `SATQUERY_API_KEY` environment variable.

## Rationale

1. **Prototype-appropriate**: OAuth2 requires an authorization server, token refresh flows, and user sessions — all unnecessary overhead for a demo platform.
2. **Transparent**: The demo key `satquery-demo-key-2024` can be safely shared in documentation without security risk.
3. **Configurable**: `SATQUERY_API_KEY=your-secret` in `.env` immediately hardens the deployment without code changes.
4. **FastAPI middleware**: Implemented as an HTTP middleware layer, so it applies to all future routes automatically.

## Migration Path

Production hardening requires: OAuth2/OIDC with `python-jose`, role-based access control (RBAC), audit logging (`who exported what, when`), and rotating API keys per organization.

## Consequences

- **Positive**: Zero friction for demos, works in all HTTP clients, configurable.
- **Negative**: Single shared key, no per-user audit trail.
