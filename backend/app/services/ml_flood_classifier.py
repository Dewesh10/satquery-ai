"""
ml_flood_classifier.py — Multi-Sensor Random Forest Flood Classifier (Synthetic Validation):

IMPORTANT DISCLAIMER:
The training and test sets are both generated from numpy distributions calibrated to
published SAR backscatter physics — they are NOT real Sentinel-1 GRD product pixels.
The train/test split uses different random seeds (Bolivar-like vs Assam-like noise levels)
to simulate geographic generalisation, but this is not equivalent to evaluating on
real out-of-distribution image chips.

The metric (+40 IoU points over cloudy-scene NDWI) reflects algorithmic behaviour
on synthetic data, not a reproducible benchmark score on actual satellite imagery.

Real evaluation path:
  1. Download Sen1Floods11 flood chip pairs (gs://sen1floods11_dataset/)
  2. Load VV/VH GeoTIFFs + hand-labelled water masks
  3. Train on events listed in train_split.csv, evaluate on test_split.csv
  4. Replace this module's _train_and_evaluate() accordingly
"""
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, jaccard_score
from typing import Dict, Any

class MultiSensorFloodMLModel:
    def __init__(self):
        self.clf = RandomForestClassifier(n_estimators=30, max_depth=5, random_state=42)
        self.is_trained = False
        self.evaluation_results: Dict[str, Any] = {}
        self._train_and_evaluate()

    def _train_and_evaluate(self):
        """
        Trains on synthetic Event A distribution (Bolivar-like noise level) and
        evaluates on a separate synthetic Event B distribution (heavier Assam monsoon
        cloud degradation on NDWI). Both use numpy-generated arrays, not real pixels.
        """
        np.random.seed(42)
        n_train = 2000
        n_test  = 1000

        # Synthetic Event A (training): moderate cloud, clean SAR
        train_water = np.random.choice([0, 1], size=n_train, p=[0.75, 0.25])
        train_vv    = np.where(train_water == 1, np.random.normal(-20.5, 2.4, n_train), np.random.normal(-11.8, 3.0, n_train))
        train_vh    = np.where(train_water == 1, np.random.normal(-26.5, 2.6, n_train), np.random.normal(-18.2, 3.2, n_train))
        train_ratio = train_vv - train_vh
        train_ndwi  = np.where(train_water == 1, np.random.normal(0.38, 0.20, n_train), np.random.normal(-0.22, 0.25, n_train))
        X_train = np.column_stack([train_vv, train_vh, train_ratio, train_ndwi])
        y_train = train_water

        # Synthetic Event B (test): heavier monsoonal cloud degrades NDWI significantly
        test_water  = np.random.choice([0, 1], size=n_test, p=[0.72, 0.28])
        test_vv     = np.where(test_water == 1, np.random.normal(-20.1, 2.7, n_test), np.random.normal(-12.2, 3.4, n_test))
        test_vh     = np.where(test_water == 1, np.random.normal(-26.0, 2.8, n_test), np.random.normal(-18.5, 3.5, n_test))
        test_ratio  = test_vv - test_vh
        test_ndwi   = np.where(test_water == 1, np.random.normal(0.26, 0.26, n_test), np.random.normal(-0.15, 0.28, n_test))
        X_test = np.column_stack([test_vv, test_vh, test_ratio, test_ndwi])
        y_test = test_water

        self.clf.fit(X_train, y_train)
        self.is_trained = True

        ml_preds = self.clf.predict(X_test)
        ml_prec  = float(precision_score(y_test, ml_preds))
        ml_rec   = float(recall_score(y_test, ml_preds))
        ml_iou   = float(jaccard_score(y_test, ml_preds))
        ml_f1    = float(2 * ml_prec * ml_rec / (ml_prec + ml_rec)) if (ml_prec + ml_rec) > 0 else 0.0

        # Classical NDWI threshold (> 0.15) on the same cloudy-scene test distribution
        classical_preds = (X_test[:, 3] > 0.15).astype(int)
        c_prec = float(precision_score(y_test, classical_preds))
        c_rec  = float(recall_score(y_test, classical_preds))
        c_iou  = float(jaccard_score(y_test, classical_preds))
        c_f1   = float(2 * c_prec * c_rec / (c_prec + c_rec)) if (c_prec + c_rec) > 0 else 0.0

        iou_points_gain   = round((ml_iou - c_iou) * 100, 2)
        relative_gain_pct = round(((ml_iou - c_iou) / c_iou) * 100, 1)

        self.evaluation_results = {
            "evaluation_type": "SYNTHETIC_PIPELINE_VALIDATION",
            "disclaimer": "Scores computed on synthetic numpy arrays, NOT real Sentinel-1 GRD pixels. Algorithmic behaviour validation only.",
            "model_type": "RandomForestClassifier (n_estimators=30, max_depth=5)",
            "evaluation_protocol": "Different synthetic distributions for train (Event A) and test (Event B)",
            "training_samples": n_train,
            "test_samples":     n_test,
            "feature_names": ["Sentinel-1 SAR VV (dB)", "Sentinel-1 SAR VH (dB)", "VV/VH Polarimetric Delta", "Sentinel-2 Optical NDWI"],
            "feature_importances": {
                "sar_vv_db":          round(float(self.clf.feature_importances_[0]), 4),
                "sar_vh_db":          round(float(self.clf.feature_importances_[1]), 4),
                "polarimetric_ratio": round(float(self.clf.feature_importances_[2]), 4),
                "optical_ndwi":       round(float(self.clf.feature_importances_[3]), 4)
            },
            "ml_model_metrics": {
                "precision": round(ml_prec, 4),
                "recall":    round(ml_rec, 4),
                "f1_score":  round(ml_f1, 4),
                "iou_jaccard": round(ml_iou, 4)
            },
            "classical_ndwi_baseline": {
                "precision": round(c_prec, 4),
                "recall":    round(c_rec, 4),
                "f1_score":  round(c_f1, 4),
                "iou_jaccard": round(c_iou, 4)
            },
            "gain_summary": {
                "iou_points_gain":   f"+{iou_points_gain} points (synthetic)",
                "relative_gain_pct": f"+{relative_gain_pct}% (synthetic)"
            }
        }

    def predict_flood_pixels(self, vv_arr: np.ndarray, vh_arr: np.ndarray, ndwi_arr: np.ndarray) -> Dict[str, Any]:
        orig_shape = vv_arr.shape
        ratio      = vv_arr - vh_arr
        X_eval     = np.column_stack([vv_arr.flatten(), vh_arr.flatten(), ratio.flatten(), ndwi_arr.flatten()])
        preds      = self.clf.predict(X_eval).reshape(orig_shape)
        water_px   = int(np.sum(preds == 1))
        total_px   = int(preds.size)
        return {
            "classified_water_pixels": water_px,
            "water_fraction_pct":      round((water_px / total_px) * 100.0, 2),
            "model_status":            "REAL_SKLEARN_INFERENCE_COMPLETE"
        }

    def get_evaluation(self) -> Dict[str, Any]:
        return self.evaluation_results

ml_flood_engine = MultiSensorFloodMLModel()
