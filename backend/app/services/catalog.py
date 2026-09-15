from typing import Dict, List, Any
from app.core.data_store import data_store

class CatalogService:
    def get_preset_scenes(self, preset_id: str) -> List[Dict[str, Any]]:
        return data_store.search_scenes(preset_id=preset_id)

    def search(self, bbox: List[float] = None, preset_id: str = None, cloud_cover: float = 100.0) -> Dict[str, Any]:
        scenes = data_store.search_scenes(preset_id=preset_id, bbox=bbox, max_clouds=cloud_cover)
        return {
            "count": len(scenes),
            "scenes": scenes
        }

catalog_service = CatalogService()
