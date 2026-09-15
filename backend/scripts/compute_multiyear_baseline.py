"""
Multi-Year Empirical Phenological Baseline Engine
SatQuery AI — Autonomous Earth Observation Platform

Queries multiple historical Sentinel-2 scenes (2021-2023) for Assam pilot region,
extracts real sub-window GeoTIFF pixel arrays, computes NDVI matrices,
and calculates true empirical seasonal mean (μ) and standard deviation (σ).
"""

import urllib.request
import io
import json
import ssl
import tifffile
import numpy as np

def compute_empirical_baseline():
    scenes = [
        {'year': '2021-04 (Pre-monsoon)', 'scene_id': 'S2A_46RDQ_20210428_0_L2A', 'b04': 'https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/46/R/DQ/2021/4/S2A_46RDQ_20210428_0_L2A/B04.tif', 'b08': 'https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/46/R/DQ/2021/4/S2A_46RDQ_20210428_0_L2A/B08.tif'},
        {'year': '2022-04 (Pre-monsoon)', 'scene_id': 'S2B_46RDP_20220428_0_L2A', 'b04': 'https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/46/R/DP/2022/4/S2B_46RDP_20220428_0_L2A/B04.tif', 'b08': 'https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/46/R/DP/2022/4/S2B_46RDP_20220428_0_L2A/B08.tif'},
        {'year': '2023-04 (Pre-monsoon)', 'scene_id': 'S2A_46RDP_20230428_0_L2A', 'b04': 'https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/46/R/DP/2023/4/S2A_46RDP_20230428_0_L2A/B04.tif', 'b08': 'https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/46/R/DP/2023/4/S2A_46RDP_20230428_0_L2A/B08.tif'},
        {'year': '2023-12 (Post-monsoon)', 'scene_id': 'S2B_46RDP_20231229_0_L2A', 'b04': 'https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/46/R/DP/2023/12/S2B_46RDP_20231229_0_L2A/B04.tif', 'b08': 'https://sentinel-cogs.s3.us-west-2.amazonaws.com/sentinel-s2-l2a-cogs/46/R/DP/2023/12/S2B_46RDP_20231229_0_L2A/B08.tif'}
    ]

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    headers = {'Range': 'bytes=0-1048576', 'User-Agent': 'SatQuery-AI/2.1'}

    print("Fetching multi-year Sentinel-2 COG GeoTIFF rasters for Assam Pilot Region...")
    ndvis = []
    for sc in scenes:
        r4 = urllib.request.Request(sc['b04'], headers=headers)
        r8 = urllib.request.Request(sc['b08'], headers=headers)
        d4 = urllib.request.urlopen(r4, context=ctx).read()
        d8 = urllib.request.urlopen(r8, context=ctx).read()
        
        with tifffile.TiffFile(io.BytesIO(d4)) as tf4, tifffile.TiffFile(io.BytesIO(d8)) as tf8:
            b4 = tf4.pages[-1].asarray()
            b8 = tf8.pages[-1].asarray()
            mask = (b4 > 0) & (b8 > 0)
            ys, xs = np.where(mask)
            cy, cx = ys[len(ys)//2], xs[len(xs)//2]
            s4 = b4[cy:cy+5, cx:cx+5].astype(float) / 10000.0
            s8 = b8[cy:cy+5, cx:cx+5].astype(float) / 10000.0
            ndvi = (s8 - s4) / (s8 + s4 + 1e-6)
            mean_v = float(np.mean(ndvi))
            sc['mean_ndvi'] = mean_v
            ndvis.append(ndvi)
            print(f"  • {sc['scene_id']} ({sc['year']}): Mean NDVI = {mean_v:.4f}")

    deltas = [ndvis[i] - ndvis[0] for i in range(1, len(ndvis))]
    all_deltas = np.array(deltas)

    empirical_mu = float(np.mean(all_deltas))
    empirical_sigma = float(np.std(all_deltas))

    result = {
        "pilot_region": "Assam Brahmaputra Basin (26.25° N, 92.00° E)",
        "years_sampled": ["2021", "2022", "2023"],
        "scenes": scenes,
        "empirical_seasonal_stats": {
            "mu_seasonal": round(empirical_mu, 6),
            "sigma_seasonal": round(empirical_sigma, 6),
            "z_score_formula": "ΔZ = (ΔNDVI - μ_seasonal) / σ_seasonal",
            "threshold_z": 2.5
        }
    }

    print("\n=== MULTI-YEAR EMPIRICAL BASELINE COMPUTATION COMPLETE ===")
    print(json.dumps(result, indent=2))
    return result

if __name__ == "__main__":
    compute_empirical_baseline()
