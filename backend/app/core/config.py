import os

class Settings:
    PROJECT_NAME: str = "SatQuery AI — Earth Observation Copilot"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api"
    DEBUG: bool = True
    API_KEY: str = os.getenv("SATQUERY_API_KEY", "satquery-demo-key-2024")
    
    PRESETS = {
        "dubai_urban": {
            "name": "Dubai Built-Up Growth (2018 vs 2024)",
            "category": "Urban Growth",
            "center": [25.08, 55.20],
            "zoom": 12,
            "bbox": [55.12, 24.95, 55.35, 25.15],
            "dates": ["2018-03-15", "2024-02-20"],
            "sensors": ["Sentinel-2A MSI", "Sentinel-2B MSI"],
            "suggested_prompt": "Show built-up expansion in Dubai between March 2018 and February 2024 and calculate total new infrastructure area."
        },
        "newyork_urban": {
            "name": "New York Metropolitan Built-Up Expansion (2018 vs 2024)",
            "category": "Urban Growth",
            "center": [40.7128, -74.0060],
            "zoom": 12,
            "bbox": [-74.15, 40.60, -73.85, 40.85],
            "dates": ["2018-04-10", "2024-04-15"],
            "sensors": ["Sentinel-2A MSI", "Sentinel-2B MSI"],
            "suggested_prompt": "Show built-up growth and shoreline infrastructure development in New York between 2018 and 2024"
        },
        "india_delhi": {
            "name": "India NCR (Delhi-Gurugram-Noida) Urban Expansion",
            "category": "Urban Growth",
            "center": [28.6139, 77.2090],
            "zoom": 11,
            "bbox": [76.95, 28.40, 77.45, 28.80],
            "dates": ["2019-02-10", "2024-02-15"],
            "sensors": ["Sentinel-2A MSI", "Landsat-9 OLI-2"],
            "suggested_prompt": "Show urban expansion and built-up growth across India NCR region between 2019 and 2024"
        },
        "india_mumbai": {
            "name": "Mumbai Coastal Land Reclamation & Port Expansion",
            "category": "Coastal Infrastructure",
            "center": [19.0760, 72.8777],
            "zoom": 12,
            "bbox": [72.75, 18.90, 73.05, 19.25],
            "dates": ["2018-01-15", "2024-01-20"],
            "sensors": ["Sentinel-1 SAR", "Sentinel-2B MSI"],
            "suggested_prompt": "Analyze coastal land reclamation and infrastructure growth in Mumbai"
        },
        "amazon_deforestation": {
            "name": "Amazon Basin Canopy Loss (2020 vs 2024)",
            "category": "Deforestation",
            "center": [-10.30, -62.60],
            "zoom": 11,
            "bbox": [-62.80, -10.50, -62.40, -10.10],
            "dates": ["2020-07-10", "2024-07-12"],
            "sensors": ["Landsat-8 OLI", "Landsat-9 OLI-2"],
            "suggested_prompt": "Detect forest clearing and canopy loss in Rondonia Amazon between July 2020 and July 2024."
        },
        "lake_mead": {
            "name": "Lake Mead Water Body Shrinkage (2015 vs 2023)",
            "category": "Water Monitoring",
            "center": [36.12, -114.60],
            "zoom": 11,
            "bbox": [-114.80, 36.00, -114.40, 36.25],
            "dates": ["2015-09-01", "2023-09-05"],
            "sensors": ["Sentinel-2A MSI", "Sentinel-2B MSI"],
            "suggested_prompt": "Analyze surface water retreat and exposed shoreline bathymetry at Lake Mead from 2015 to 2023."
        },
        "assam_flood": {
            "name": "Assam Brahmaputra Monsoon Flood (SAR Radar)",
            "category": "Disaster Response",
            "center": [26.30, 92.65],
            "zoom": 11,
            "bbox": [92.40, 26.10, 92.90, 26.50],
            "dates": ["2023-05-10", "2023-07-18"],
            "sensors": ["Sentinel-1A SAR (C-band)", "Sentinel-2 MSI"],
            "suggested_prompt": "Use SAR radar imagery to isolate submerged cropland and flooded settlements in Assam during July 2023 monsoon."
        },
        "singapore_maritime": {
            "name": "Singapore Strait Maritime Vessel Traffic",
            "category": "Infrastructure & Logistics",
            "center": [1.26, 103.82],
            "zoom": 13,
            "bbox": [103.75, 1.20, 103.90, 1.32],
            "dates": ["2024-06-01", "2024-06-15"],
            "sensors": ["Capella SAR Spotlight", "PlanetScope Dove 3m"],
            "suggested_prompt": "Detect container ships, identify anchored vessels, and map berth occupancy in Singapore port corridor."
        },
        "heavy_cloud_failure": {
            "name": "⚠️ Heavy Monsoon Cloud Cover (Model Refusal Demo)",
            "category": "Adversarial Test",
            "center": [-3.10, -60.02],
            "zoom": 11,
            "bbox": [-60.20, -3.20, -59.80, -3.00],
            "dates": ["2023-11-01", "2023-11-15"],
            "sensors": ["Sentinel-2B MSI (94.2% Clouds)"],
            "suggested_prompt": "Detect forest clearing in Amazon Basin during November heavy rainfall."
        }
    }

settings = Settings()
