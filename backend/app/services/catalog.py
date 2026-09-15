import urllib.request
import json
from typing import Dict, List, Any
from app.core.data_store import data_store

class CatalogService:
    def search_live_stac(self, bbox: List[float], max_clouds: float = 100.0) -> List[Dict[str, Any]]:
        try:
            url = "https://earth-search.aws.element84.com/v1/search"
            payload = {
                "collections": ["sentinel-2-l2a"],
                "bbox": bbox,
                "datetime": "2022-01-01T00:00:00Z/2024-12-31T23:59:59Z",
                "limit": 4
            }
            req = urllib.request.Request(
                url, 
                data=json.dumps(payload).encode('utf-8'),
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'SatQueryAI-LiveSTAC/2.0 (contact@satquery.ai)'
                }
            )
            with urllib.request.urlopen(req, timeout=3.5) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode('utf-8'))
                    items = data.get("features", [])
                    stac_scenes = []
                    for item in items:
                        props = item.get("properties", {})
                        assets = item.get("assets", {})
                        cloud_pct = props.get("eo:cloud_cover", 0.0)
                        if cloud_pct > max_clouds:
                            continue
                        
                        thumb = assets.get("thumbnail", {}).get("href") or assets.get("rendered_preview", {}).get("href") or "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=600&q=80"
                        
                        stac_scenes.append({
                            "id": item.get("id"),
                            "collection": item.get("collection", "sentinel-2-l2a"),
                            "preset_id": "live_stac",
                            "mission_mode": "LIVE_SATELLITE_CATALOG",
                            "title": f"Live Sentinel-2 Scene ({props.get('datetime', '')[:10]})",
                            "datetime": props.get("datetime", "2024-01-01T00:00:00Z"),
                            "sensor": props.get("platform", "Sentinel-2B"),
                            "modality": "OPTICAL",
                            "cloud_cover": round(cloud_pct, 2),
                            "gsd_meters": 10.0,
                            "bbox": item.get("bbox", bbox),
                            "center": [(item.get("bbox", bbox)[1] + item.get("bbox", bbox)[3]) / 2, (item.get("bbox", bbox)[0] + item.get("bbox", bbox)[2]) / 2],
                            "bands": ["B02 (Blue)", "B03 (Green)", "B04 (Red)", "B08 (NIR)", "B11 (SWIR1)"],
                            "sun_elevation": round(props.get("view:sun_elevation", 55.0), 1),
                            "thumbnail": thumb,
                            "stac_url": item.get("links", [{}])[0].get("href", f"stac://earth-search/{item.get('id')}")
                        })
                    if stac_scenes:
                        return stac_scenes
        except Exception as e:
            print("Live STAC Search bypassed or timed out:", e)
        return []

    def get_preset_scenes(self, preset_id: str) -> List[Dict[str, Any]]:
        return data_store.search_scenes(preset_id=preset_id)

    def search(self, bbox: List[float] = None, preset_id: str = None, cloud_cover: float = 100.0) -> Dict[str, Any]:
        if bbox and len(bbox) == 4:
            live_scenes = self.search_live_stac(bbox, cloud_cover)
            if live_scenes:
                return {"count": len(live_scenes), "scenes": live_scenes, "is_live_stac": True}

        scenes = data_store.search_scenes(preset_id=preset_id, bbox=bbox, max_clouds=cloud_cover)
        return {
            "count": len(scenes),
            "scenes": scenes,
            "is_live_stac": False
        }

catalog_service = CatalogService()
