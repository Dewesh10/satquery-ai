"""
cloud_mask.py — Sentinel-2 Scene Classification Layer (SCL) Cloud Masking:
Filters out atmospheric interference using the standard ESA Sentinel-2 L2A SCL band:
- 0: NO_DATA (masked)
- 1: SATURATED_OR_DEFECTIVE (masked)
- 2: DARK_AREA_PIXELS (valid)
- 3: CLOUD_SHADOWS (masked)
- 4: VEGETATION (valid)
- 5: NOT_VEGETATED (valid)
- 6: WATER (valid)
- 7: UNCLASSIFIED (valid)
- 8: CLOUD_MEDIUM_PROBABILITY (masked)
- 9: CLOUD_HIGH_PROBABILITY (masked)
- 10: THIN_CIRRUS (masked)
- 11: SNOW (valid / configurable)
"""
from typing import Tuple, Dict, Any
import numpy as np

# Standard SCL classes that degrade optical surface reflectance
SCL_MASK_CLASSES = {0, 1, 3, 8, 9, 10}

def compute_scl_valid_mask(scl_arr: np.ndarray, mask_classes=SCL_MASK_CLASSES) -> np.ndarray:
    """
    Returns boolean array where True = clear/valid surface observation,
    False = contaminated by cloud, cloud shadow, cirrus, or missing data.
    """
    valid_mask = np.ones(scl_arr.shape, dtype=bool)
    for cls in mask_classes:
        valid_mask &= (scl_arr != cls)
    return valid_mask

def apply_scl_cloud_mask(
    band_arr: np.ndarray,
    scl_arr: np.ndarray,
    fill_value: float = np.nan
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Applies SCL mask to an optical spectral band or index array.
    Returns the masked array and quality statistics (cloud-free fraction, valid pixel count).
    """
    valid_mask = compute_scl_valid_mask(scl_arr)
    total_pixels = int(scl_arr.size)
    valid_pixels = int(np.sum(valid_mask))
    cloud_pixels = total_pixels - valid_pixels
    cloud_free_fraction = float(valid_pixels / total_pixels) if total_pixels > 0 else 0.0

    masked_arr = np.where(valid_mask, band_arr, fill_value)

    stats = {
        "total_pixels": total_pixels,
        "valid_pixels": valid_pixels,
        "cloud_shadow_pixels": cloud_pixels,
        "cloud_free_fraction": round(cloud_free_fraction, 4),
        "cloud_cover_pct": round((1.0 - cloud_free_fraction) * 100.0, 2),
        "quality_status": "EXCELLENT" if cloud_free_fraction > 0.85 else ("ACCEPTABLE" if cloud_free_fraction > 0.60 else "DEGRADED_HEAVY_CLOUDS")
    }
    return masked_arr, stats
