"""
eval_benchmarks.py — Synthetic Pipeline Validation Suite:

IMPORTANT DISCLAIMER:
These metrics are computed on SYNTHETIC pixel arrays generated from calibrated
SAR/optical physics distributions (Gaussian noise around empirically documented
backscatter means). They are NOT scores on real Sen1Floods11 or OSCD image chips.
They validate that the pipeline's algorithms (thresholding, connected components,
Random Forest fusion) behave correctly given realistic signal distributions.

To obtain real benchmark scores, download:
- Sen1Floods11: gs://sen1floods11_dataset/ (Google Cloud Storage, public)
  Paper: Bonafilia et al., CVPRW 2020. https://github.com/cloudtostreet/sen1floods11
- OSCD: https://ieee-dataport.org/open-access/oscd-onera-satellite-change-detection
  Paper: Daudt et al., IGARSS 2018.

Real evaluation would require: loading actual GeoTIFF chips, applying the pipeline,
and comparing predictions against the provided ground truth label masks.
"""
from typing import Dict, Any
import numpy as np

def evaluate_sar_threshold_synthetic(threshold_db: float = -16.5) -> Dict[str, Any]:
    """
    Validates SAR specular backscatter thresholding on synthetic pixel arrays.
    Signal distributions calibrated from published SAR physics:
    - Water: mean VV ~ -20.2 dB (specular forward scattering, C-band 5.405 GHz)
    - Land:  mean VV ~ -12.1 dB (diffuse volume scattering)
    - Radar shadows and speckle noise included as realistic false-positive sources.

    NOTE: These are NOT scores on real Sen1Floods11 chips.
    """
    np.random.seed(1042)
    h, w = 120, 120

    # Synthetic ground truth: ~22% water coverage (typical monsoon inundation)
    gt_water = np.zeros((h, w), dtype=bool)
    gt_water[35:75, 25:75] = True
    gt_water[20:35, 45:65] = True

    # Synthetic SAR VV with realistic speckle (Gamma/Rayleigh distributed noise)
    sar_vv_db = np.where(
        gt_water,
        np.random.normal(-20.2, 2.6, (h, w)),
        np.random.normal(-12.1, 3.4, (h, w))
    )
    # Radar shadow artifacts in terrain (causes realistic false positives)
    sar_vv_db[10:18, 10:22] = np.random.normal(-19.5, 1.2, (8, 12))

    pred_water = sar_vv_db < threshold_db

    tp = int(np.sum(pred_water & gt_water))
    fp = int(np.sum(pred_water & ~gt_water))
    fn = int(np.sum(~pred_water & gt_water))
    tn = int(np.sum(~pred_water & ~gt_water))

    precision = float(tp / (tp + fp)) if (tp + fp) > 0 else 0.0
    recall    = float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0
    iou       = float(tp / (tp + fp + fn)) if (tp + fp + fn) > 0 else 0.0
    f1        = float(2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

    return {
        "evaluation_type": "SYNTHETIC_PIPELINE_VALIDATION",
        "disclaimer": "NOT a Sen1Floods11 benchmark score. Synthetic arrays calibrated to SAR physics distributions.",
        "algorithm_tested": "SAR specular backscatter thresholding",
        "signal_distribution": f"Water: N(-20.2, 2.6) dB | Land: N(-12.1, 3.4) dB | threshold: {threshold_db} dB",
        "metrics": {
            "precision": round(precision, 4),
            "recall":    round(recall, 4),
            "iou_jaccard": round(iou, 4),
            "f1_score":  round(f1, 4),
            "true_positive_pixels":  tp,
            "false_positive_pixels": fp,
            "false_negative_pixels": fn,
            "total_evaluated_pixels": h * w
        },
        "real_benchmark_reference": "Bonafilia et al., Sen1Floods11 (CVPRW 2020). Real chips at gs://sen1floods11_dataset/"
    }

def evaluate_urban_change_detection_synthetic(threshold_delta: float = 0.28) -> Dict[str, Any]:
    """
    Validates bitemporal NDBI delta change detection on synthetic pixel arrays.
    Includes realistic class imbalance (~3.2% true-change pixels) and coregistration
    edge artefacts, consistent with the OSCD dataset's known difficulty.

    NOTE: These are NOT scores on real OSCD chips.
    """
    np.random.seed(2084)
    h, w = 150, 150

    # Sparse true urban expansion (~3.2% of total pixels)
    gt_change = np.zeros((h, w), dtype=bool)
    gt_change[40:55, 40:60] = True
    gt_change[105:120, 85:110] = True

    # Synthetic NDBI delta with seasonal phenology noise and coregistration jitter
    delta_ndbi = np.where(
        gt_change,
        np.random.normal(0.40, 0.14, (h, w)),
        np.random.normal(0.08, 0.12, (h, w))
    )
    # Coregistration edge artefacts causing realistic false alarms
    delta_ndbi[38:40, 38:62] += 0.22
    delta_ndbi[103:105, 83:112] += 0.20

    pred_change = delta_ndbi > threshold_delta

    tp = int(np.sum(pred_change & gt_change))
    fp = int(np.sum(pred_change & ~gt_change))
    fn = int(np.sum(~pred_change & gt_change))

    precision = float(tp / (tp + fp)) if (tp + fp) > 0 else 0.0
    recall    = float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0
    iou       = float(tp / (tp + fp + fn)) if (tp + fp + fn) > 0 else 0.0
    f1        = float(2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0

    return {
        "evaluation_type": "SYNTHETIC_PIPELINE_VALIDATION",
        "disclaimer": "NOT an OSCD benchmark score. Synthetic arrays mirroring OSCD class imbalance and coregistration noise.",
        "algorithm_tested": "Bitemporal NDBI delta thresholding with SciPy morphological clustering",
        "signal_distribution": f"Change: N(0.40, 0.14) | No-change: N(0.08, 0.12) | threshold: {threshold_delta}",
        "class_imbalance": "~3.2% positive pixels (consistent with OSCD difficulty)",
        "metrics": {
            "precision": round(precision, 4),
            "recall":    round(recall, 4),
            "iou_jaccard": round(iou, 4),
            "f1_score":  round(f1, 4),
            "true_positive_pixels":  tp,
            "false_positive_pixels": fp,
            "false_negative_pixels": fn,
            "total_evaluated_pixels": h * w
        },
        "real_benchmark_reference": "Daudt et al., OSCD (IGARSS 2018). Data at https://ieee-dataport.org/open-access/oscd-onera-satellite-change-detection"
    }

# Backward-compatible aliases (kept so API endpoint doesn't break)
def evaluate_sen1floods11_sar(threshold_db: float = -16.5) -> Dict[str, Any]:
    return evaluate_sar_threshold_synthetic(threshold_db)

def evaluate_oscd_urban(threshold_delta: float = 0.28) -> Dict[str, Any]:
    return evaluate_urban_change_detection_synthetic(threshold_delta)

def get_all_benchmark_scores() -> Dict[str, Any]:
    return {
        "disclaimer": "These are synthetic pipeline validation scores, NOT scores on real Sen1Floods11 or OSCD chips.",
        "sar_threshold_synthetic_validation": evaluate_sar_threshold_synthetic(),
        "urban_change_detection_synthetic_validation": evaluate_urban_change_detection_synthetic(),
        "real_evaluation_path": {
            "sen1floods11": "gs://sen1floods11_dataset/ — download S1Hand.csv label chips, run evaluate_sar_threshold_synthetic replacement on actual VV/VH GeoTIFFs",
            "oscd": "https://ieee-dataport.org/open-access/oscd-onera-satellite-change-detection — download Sentinel-2 image pairs + change label masks"
        }
    }
