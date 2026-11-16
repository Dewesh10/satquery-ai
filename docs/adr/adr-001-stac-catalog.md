# ADR-001 — Data Source: Earth Search (AWS Element84) STAC API

**Date**: 2024-11-05  
**Status**: Accepted  
**Deciders**: SatQuery AI core team

## Context

SatQuery AI needs access to multi-temporal satellite imagery metadata for change detection analysis. Options considered:

| Option | Cost | Auth Required | COG Support | Coverage |
|---|---|---|---|---|
| **Earth Search (AWS Element84)** | Free | None | ✅ Native | Sentinel-2 L2A global |
| Copernicus Data Space | Free | OAuth2 | ✅ | Sentinel-2 global |
| Planet API | Paid ($) | API Key | ✅ | Planet Dove global |
| SentinelHub | Paid ($) | OAuth2 | ✅ | Multi-sensor |
| NASA CMR STAC | Free | None | Partial | Landsat, MODIS |

## Decision

Use **Earth Search (AWS Element84)** at `https://earth-search.aws.element84.com/v1`.

## Rationale

1. **Zero-auth, zero-cost**: No API key registration required. Works immediately in any environment.
2. **COG-native**: All assets are Cloud-Optimized GeoTIFFs, enabling HTTP Range Request band reads without full scene download.
3. **Sentinel-2 L2A**: Atmospherically corrected surface reflectance — the right starting point for NDVI/NDWI spectral index math.
4. **STAC-compliant**: Industry-standard metadata format; switching to another STAC catalog later is a one-line change.

## Consequences

- **Positive**: Zero infrastructure cost, global coverage, real scene IDs and acquisition metadata.
- **Negative**: Dependent on AWS infrastructure availability; no Sentinel-1 SAR (would require Copernicus).
- **Limitation**: COG Range Requests are limited to overview tiles in demo mode to avoid high egress.
