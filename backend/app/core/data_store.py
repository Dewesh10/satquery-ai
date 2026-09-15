from typing import Dict, List, Any

class STACDataStore:
    def __init__(self):
        self.scenes: List[Dict[str, Any]] = [
            {
                "id": "S2A_MSIL2A_20180315T064019_N0206_R077_T40RCN",
                "collection": "sentinel-2-l2a",
                "preset_id": "dubai_urban",
                "mission_mode": "URBAN_GROWTH",
                "title": "Dubai Sentinel-2A Optical Scene (Pre-growth Baseline)",
                "datetime": "2018-03-15T06:40:19Z",
                "sensor": "Sentinel-2A MSI (Multi-Spectral Instrument)",
                "modality": "OPTICAL",
                "cloud_cover": 0.42,
                "gsd_meters": 10.0,
                "orbit_direction": "DESCENDING",
                "orbit_number": 77,
                "bbox": [55.10, 24.90, 55.40, 25.20],
                "center": [25.08, 55.20],
                "bands": ["B02 (Blue)", "B03 (Green)", "B04 (Red)", "B08 (NIR)", "B11 (SWIR1)", "B12 (SWIR2)"],
                "sun_elevation": 58.4,
                "sun_azimuth": 142.1,
                "histogram": {"red": [12, 45, 120, 200, 80], "nir": [5, 20, 85, 190, 110]},
                "thumbnail": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=600&q=80",
                "stac_url": "stac://sentinel-s2-l2a/S2A_MSIL2A_20180315"
            },
            {
                "id": "S2B_MSIL2A_20240220T064021_N0510_R077_T40RCN",
                "collection": "sentinel-2-l2a",
                "preset_id": "dubai_urban",
                "mission_mode": "URBAN_GROWTH",
                "title": "Dubai Sentinel-2B Optical Scene (Post-growth)",
                "datetime": "2024-02-20T06:40:21Z",
                "sensor": "Sentinel-2B MSI (Multi-Spectral Instrument)",
                "modality": "OPTICAL",
                "cloud_cover": 0.15,
                "gsd_meters": 10.0,
                "orbit_direction": "DESCENDING",
                "orbit_number": 77,
                "bbox": [55.10, 24.90, 55.40, 25.20],
                "center": [25.08, 55.20],
                "bands": ["B02 (Blue)", "B03 (Green)", "B04 (Red)", "B08 (NIR)", "B11 (SWIR1)", "B12 (SWIR2)"],
                "sun_elevation": 49.8,
                "sun_azimuth": 146.5,
                "histogram": {"red": [8, 30, 150, 240, 120], "nir": [10, 35, 95, 210, 140]},
                "thumbnail": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=600&q=80",
                "stac_url": "stac://sentinel-s2-l2a/S2B_MSIL2A_20240220"
            },
            {
                "id": "LC08_L2SP_231067_20200710_20200722_02_T1",
                "collection": "landsat-8-c2-l2",
                "preset_id": "amazon_deforestation",
                "mission_mode": "AGRICULTURE_FORESTRY",
                "title": "Amazon Rondonia Landsat-8 Scene (Baseline Canopy)",
                "datetime": "2020-07-10T14:15:32Z",
                "sensor": "Landsat-8 OLI (Operational Land Imager)",
                "modality": "OPTICAL",
                "cloud_cover": 2.10,
                "gsd_meters": 30.0,
                "orbit_direction": "DESCENDING",
                "orbit_number": 231,
                "bbox": [-62.90, -10.60, -62.30, -10.00],
                "center": [-10.30, -62.60],
                "bands": ["SR_B2", "SR_B3", "SR_B4", "SR_B5 (NIR)", "SR_B6 (SWIR1)", "ST_B10 (Thermal)"],
                "sun_elevation": 51.2,
                "sun_azimuth": 54.8,
                "histogram": {"ndvi": [0.1, 0.3, 0.78, 0.85, 0.60]},
                "thumbnail": "https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?auto=format&fit=crop&w=600&q=80",
                "stac_url": "stac://landsat-c2-l2/LC08_20200710"
            },
            {
                "id": "LC09_L2SP_231067_20240712_20240714_02_T1",
                "collection": "landsat-9-c2-l2",
                "preset_id": "amazon_deforestation",
                "mission_mode": "AGRICULTURE_FORESTRY",
                "title": "Amazon Rondonia Landsat-9 Scene (Canopy Loss)",
                "datetime": "2024-07-12T14:16:05Z",
                "sensor": "Landsat-9 OLI-2",
                "modality": "OPTICAL",
                "cloud_cover": 1.45,
                "gsd_meters": 30.0,
                "orbit_direction": "DESCENDING",
                "orbit_number": 231,
                "bbox": [-62.90, -10.60, -62.30, -10.00],
                "center": [-10.30, -62.60],
                "bands": ["SR_B2", "SR_B3", "SR_B4", "SR_B5 (NIR)", "SR_B6 (SWIR1)", "ST_B10 (Thermal)"],
                "sun_elevation": 50.8,
                "sun_azimuth": 55.2,
                "histogram": {"ndvi": [0.4, 0.55, 0.61, 0.42, 0.20]},
                "thumbnail": "https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?auto=format&fit=crop&w=600&q=80",
                "stac_url": "stac://landsat-c2-l2/LC09_20240712"
            },
            {
                "id": "S2A_MSIL2A_20150901T182021_N0202_R070_T11SKD",
                "collection": "sentinel-2-l2a",
                "preset_id": "lake_mead",
                "mission_mode": "WATER_MONITORING",
                "title": "Lake Mead Sentinel-2 Baseline High Water",
                "datetime": "2015-09-01T18:20:21Z",
                "sensor": "Sentinel-2A MSI",
                "modality": "OPTICAL",
                "cloud_cover": 0.00,
                "gsd_meters": 10.0,
                "orbit_direction": "DESCENDING",
                "orbit_number": 70,
                "bbox": [-114.90, 35.90, -114.30, 36.30],
                "center": [36.12, -114.60],
                "bands": ["B02", "B03", "B04", "B08", "B11"],
                "sun_elevation": 61.1,
                "sun_azimuth": 150.2,
                "histogram": {"ndwi": [0.8, 0.72, 0.55, 0.2]},
                "thumbnail": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=600&q=80",
                "stac_url": "stac://sentinel-s2-l2a/S2A_20150901"
            },
            {
                "id": "S1A_IW_GRDH_1SDV_20230718T115542_049472_05E12F_B22C",
                "collection": "sentinel-1-grd",
                "preset_id": "assam_flood",
                "mission_mode": "DISASTER_RESPONSE",
                "title": "Assam Brahmaputra SAR Radar Peak Flood Inundation",
                "datetime": "2023-07-18T11:55:42Z",
                "sensor": "Sentinel-1A SAR (C-Band Synthetic Aperture Radar)",
                "modality": "SAR",
                "cloud_cover": 0.0,
                "gsd_meters": 10.0,
                "orbit_direction": "ASCENDING",
                "orbit_number": 14,
                "bbox": [92.30, 26.00, 93.00, 26.60],
                "center": [26.30, 92.65],
                "bands": ["VV (Co-pol)", "VH (Cross-pol)", "VV/VH Ratio"],
                "sun_elevation": 0.0,
                "histogram": {"sar_db": [-28, -22, -15, -8, 2]},
                "thumbnail": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=600&q=80",
                "stac_url": "stac://sentinel-1-grd/S1A_20230718"
            },
            {
                "id": "CAPELLA_SPOTLIGHT_SGP_20240601_031200",
                "collection": "capella-sar-spotlight",
                "preset_id": "singapore_maritime",
                "mission_mode": "MARITIME_DEFENSE",
                "title": "Singapore Port High-Resolution SAR Spotlight",
                "datetime": "2024-06-01T03:12:00Z",
                "sensor": "Capella SAR X-Band 0.5m",
                "modality": "SAR",
                "cloud_cover": 0.0,
                "gsd_meters": 0.5,
                "orbit_direction": "ASCENDING",
                "orbit_number": 402,
                "bbox": [103.70, 1.15, 103.95, 1.35],
                "center": [1.26, 103.82],
                "bands": ["HH Single-pol High Contrast"],
                "sun_elevation": 0.0,
                "histogram": {"specular": [100, 300, 800, 1200]},
                "thumbnail": "https://images.unsplash.com/photo-1578575437130-527eed3abbec?auto=format&fit=crop&w=600&q=80",
                "stac_url": "stac://capella-sar/CAPELLA_SGP_20240601"
            }
        ]

    def search_scenes(self, preset_id: str = None, bbox: List[float] = None, max_clouds: float = 100.0) -> List[Dict[str, Any]]:
        results = []
        for s in self.scenes:
            if preset_id and s["preset_id"] == preset_id:
                if s["cloud_cover"] <= max_clouds:
                    results.append(s)
        if len(results) > 0:
            return results

        # Dynamic STAC Scenes Generator for ANY geocoded village / town / custom AOI
        return [
            {
                "id": f"S2A_MSIL2A_20190115_{preset_id or 'AOI'}",
                "collection": "sentinel-2-l2a",
                "preset_id": preset_id or "custom",
                "mission_mode": "DYNAMIC_LOCATION_MONITORING",
                "title": f"Pre-Event Baseline Optical Scene ({preset_id})",
                "datetime": "2019-01-15T06:40:00Z",
                "sensor": "Sentinel-2A MSI (10m Resolution)",
                "modality": "OPTICAL",
                "cloud_cover": 0.20,
                "gsd_meters": 10.0,
                "orbit_direction": "DESCENDING",
                "orbit_number": 77,
                "bbox": bbox or [0.0, 0.0, 0.1, 0.1],
                "center": [0.0, 0.0],
                "bands": ["B02", "B03", "B04", "B08", "B11"],
                "sun_elevation": 55.0,
                "thumbnail": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=600&q=80",
                "stac_url": "stac://sentinel-s2-l2a/dynamic_pre"
            },
            {
                "id": f"S2B_MSIL2A_20240115_{preset_id or 'AOI'}",
                "collection": "sentinel-2-l2a",
                "preset_id": preset_id or "custom",
                "mission_mode": "DYNAMIC_LOCATION_MONITORING",
                "title": f"Post-Event Analysis Optical Scene ({preset_id})",
                "datetime": "2024-01-15T06:40:00Z",
                "sensor": "Sentinel-2B MSI (10m Resolution)",
                "modality": "OPTICAL",
                "cloud_cover": 0.10,
                "gsd_meters": 10.0,
                "orbit_direction": "DESCENDING",
                "orbit_number": 77,
                "bbox": bbox or [0.0, 0.0, 0.1, 0.1],
                "center": [0.0, 0.0],
                "bands": ["B02", "B03", "B04", "B08", "B11"],
                "sun_elevation": 52.0,
                "thumbnail": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=600&q=80",
                "stac_url": "stac://sentinel-s2-l2a/dynamic_post"
            }
        ]

    def get_scene(self, scene_id: str) -> Dict[str, Any]:
        for s in self.scenes:
            if s["id"] == scene_id:
                return s
        return self.scenes[0]

data_store = STACDataStore()
