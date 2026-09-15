"""
Empirical STAC & Real GeoTIFF Pixel Extraction Script
SatQuery AI — Autonomous Earth Observation Engine

Fetches live Sentinel-2 L2A STAC metadata from AWS Element84 Earth Search,
downloads COG GeoTIFF band byte ranges for Red (B04) and NIR (B08),
extracts raw uint16 Digital Numbers, converts to Surface Reflectance,
and computes real NDVI pixel matrices.
"""

import urllib.request
import io
import json
import ssl
import tifffile
import numpy as np

def extract_real_sentinel2_pixels():
    print("1. Querying live Element84 STAC Search API...")
    stac_url = 'https://earth-search.aws.element84.com/v1/search'
    payload = {
        'collections': ['sentinel-2-l2a'],
        'bbox': [91.5, 26.0, 92.5, 26.5], # Assam, India (Brahmaputra Flood Plain)
        'datetime': '2023-01-01T00:00:00Z/2023-12-31T23:59:59Z',
        'limit': 1
    }
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    req = urllib.request.Request(stac_url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, context=ctx) as resp:
        stac_data = json.loads(resp.read().decode('utf-8'))
        
    item = stac_data['features'][0]
    scene_id = item['id']
    b04_url = item['assets']['red']['href']
    b08_url = item['assets']['nir']['href']
    
    print(f"   Scene ID: {scene_id}")
    print(f"   Red (B04) URL: {b04_url}")
    print(f"   NIR (B08) URL: {b08_url}")
    
    print("2. Fetching COG GeoTIFF byte range (1MB) from AWS S3 us-west-2...")
    headers = {'Range': 'bytes=0-1048576', 'User-Agent': 'SatQuery-AI/2.1'}
    req_b04 = urllib.request.Request(b04_url, headers=headers)
    req_b08 = urllib.request.Request(b08_url, headers=headers)
    
    with urllib.request.urlopen(req_b04, context=ctx) as r:
        b04_bytes = r.read()
    with urllib.request.urlopen(req_b08, context=ctx) as r:
        b08_bytes = r.read()
        
    print(f"   Read {len(b04_bytes)} bytes of B04, {len(b08_bytes)} bytes of B08.")
    
    print("3. Parsing GeoTIFF pages with tifffile & extracting 5x5 pixel matrix...")
    with tifffile.TiffFile(io.BytesIO(b04_bytes)) as tf_b04, tifffile.TiffFile(io.BytesIO(b08_bytes)) as tf_b08:
        b04_arr = tf_b04.pages[-1].asarray()
        b08_arr = tf_b08.pages[-1].asarray()
        
        valid_mask = (b04_arr > 0) & (b08_arr > 0)
        ys, xs = np.where(valid_mask)
        cy, cx = ys[len(ys)//2], xs[len(xs)//2]
        
        s_b04 = b04_arr[cy:cy+5, cx:cx+5]
        s_b08 = b08_arr[cy:cy+5, cx:cx+5]
        
        ref_b04 = s_b04.astype(float) / 10000.0
        ref_b08 = s_b08.astype(float) / 10000.0
        ndvi = (ref_b08 - ref_b04) / (ref_b08 + ref_b04 + 1e-6)
        
        result = {
            "scene_id": scene_id,
            "stac_collection": "sentinel-2-l2a",
            "provider": "AWS Element84 Earth Search",
            "coordinates": {"lat": 26.25, "lng": 92.00, "region": "Assam, Brahmaputra Flood Plain"},
            "raw_digital_numbers_b04_uint16": s_b04.tolist(),
            "raw_digital_numbers_b08_uint16": s_b08.tolist(),
            "surface_reflectance_b04_red": np.round(ref_b04, 4).tolist(),
            "surface_reflectance_b08_nir": np.round(ref_b08, 4).tolist(),
            "computed_ndvi_matrix": np.round(ndvi, 4).tolist(),
            "mean_red_reflectance": float(np.mean(ref_b04)),
            "mean_nir_reflectance": float(np.mean(ref_b08)),
            "mean_ndvi": float(np.mean(ndvi))
        }
        
        print("\n=== EMPIRICAL STAC GEOTIFF EXTRACTION COMPLETE ===")
        print(json.dumps(result, indent=2))
        return result

if __name__ == "__main__":
    extract_real_sentinel2_pixels()
