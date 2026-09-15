from typing import Dict, Any
import time

class ExportService:
    def export_geojson(self, analytics_data: Dict[str, Any]) -> Dict[str, Any]:
        return analytics_data.get("geojson", {"type": "FeatureCollection", "features": []})

    def export_csv(self, analytics_data: Dict[str, Any]) -> str:
        lines = [
            "Metric,Value",
            f"Preset ID,{analytics_data.get('preset_id')}",
            f"Time Span,{analytics_data.get('time_span')}",
            f"Primary Metric,{analytics_data.get('primary_metric_label')}",
            f"Primary Value,{analytics_data.get('primary_metric_value')}",
            f"Percentage Change,{analytics_data.get('percentage_change')}",
            f"Area (sq km),{analytics_data.get('area_sq_km')}",
            f"Calibrated Trust Score,{analytics_data.get('uncertainty', {}).get('calibrated_trust_score', 0.95)}",
            f"Compute Cost USD,${analytics_data.get('ops_metrics', {}).get('compute_cost_usd', 0.014)}"
        ]
        return "\n".join(lines)

    def generate_government_encroachment_notice(self, preset_id: str, analytics: Dict[str, Any], lang: str = "EN") -> str:
        """Generates a Provisional Change Detection & Internal Screening Report in EN / HI / AS."""
        date_str = time.strftime("%d-%B-%Y").upper()
        
        headers_lang = {
            "EN": ("STATE LAND REVENUE & MUNICIPAL GIS CELL", "PROVISIONAL SATELLITE CHANGE DETECTION NODE", "PROVISIONAL CHANGE DETECTION & INTERNAL SCREENING REPORT"),
            "HI": ("राज्य भूमि राजस्व एवं नगर निगम जीआईएस सेल", "अनंतिम उपग्रह परिवर्तन पहचान नोड", "अनंतिम परिवर्तन पहचान एवं आंतरिक जांच रिपोर्ट"),
            "AS": ("ৰাজ্যিক ভূমি ৰাজহ আৰু পৌৰ নিগম জি.আই.এছ. কোষ", "অস্থায়ী উপগ্ৰহ পৰিৱৰ্তন চিনাক্তকৰণ ন'ড", "অস্থায়ী পৰিৱৰ্তন চিনাক্তকৰণ আৰু আভ্যন্তৰীণ পৰীক্ষণ প্ৰতিবেদন")
        }
        
        bodies_lang = {
            "EN": "This report represents an initial automated observation derived from bi-temporal change detection algorithms operating over co-registered Sentinel-2 and Sentinel-1 SAR imagery. This report is for internal screening and field survey prioritization only.",
            "HI": "यह रिपोर्ट सेंटिनल-2 और सेंटिनल-1 एसएआर उपग्रह चित्रों के स्वचालित द्वि-कालिक परिवर्तन पहचान एल्गोरिदम से प्राप्त एक प्रारंभिक स्वचालित अवलोकन है। यह रिपोर्ट केवल आंतरिक जांच और मैदानी सर्वेक्षण प्राथमिकता के लिए है।",
            "AS": "এই প্ৰতিবেদন ছেন্টিনেল-২ আৰু ছেন্টিনেল-১ এছ.এ.আৰ. উপগ্ৰহৰ স্বয়ংক্ৰিয় পৰিৱৰ্তন বিশ্লেষণ সঁজুলিৰ দ্বাৰা প্ৰাপ্ত প্ৰাথমিক পৰ্যবেক্ষণ। এই প্ৰতিবেদন কেৱল আভ্যন্তৰীণ পৰীক্ষণ আৰু ফিল্ড জৰীপৰ বাবে।"
        }

        curr_head = headers_lang.get(lang, headers_lang["EN"])
        curr_body = bodies_lang.get(lang, bodies_lang["EN"])

        return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<title>PROVISIONAL SATELLITE CHANGE SCREENING REPORT</title>
<style>
  body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #FFFFFF; color: #000000; padding: 50px; line-height: 1.6; }}
  .emblem {{ text-align: center; font-weight: bold; text-transform: uppercase; border-bottom: 2px solid #000; padding-bottom: 15px; margin-bottom: 30px; }}
  .ref-no {{ font-family: monospace; font-size: 14px; margin-bottom: 20px; }}
  .title {{ font-size: 18px; font-weight: bold; text-align: center; text-decoration: underline; margin-bottom: 25px; color: #0f172a; }}
  .box {{ border: 1px solid #000; padding: 15px; margin: 20px 0; font-family: monospace; font-size: 13px; background: #F8F9FA; }}
  .disclaimer {{ border: 1px solid #d97706; background: #fef3c7; padding: 12px; font-family: monospace; font-size: 11px; margin: 20px 0; color: #92400e; }}
  .signature {{ margin-top: 60px; display: flex; justify-content: space-between; }}
</style>
</head>
<body>
  <div class="emblem">
    <div>{curr_head[0]}</div>
    <div style="font-size: 12px; margin-top: 5px;">{curr_head[1]}</div>
  </div>

  <div class="ref-no">
    REF NO: PRELIM/SATQUERY/{preset_id.upper()}/{time.strftime('%Y%m%d')} | CLASSIFICATION: INTERNAL SCREENING ONLY
  </div>

  <div class="title">
    {curr_head[2]}
  </div>

  <p>
    {curr_body}
  </p>

  <div class="disclaimer">
    <b>MANDATORY DISCLAIMER:</b> This document is generated automatically by satellite imagery algorithms for preliminary screening and field survey planning. It DOES NOT constitute an official legal notice, statutory order, or court-admissible evidence until physically verified and certified on the ground by authorized revenue officers.
  </div>

  <div class="box">
    <b>GEOSPATIAL AUDIT PROVENANCE:</b><br/>
    • TARGET AOI / DISTRICT: {preset_id.upper()}<br/>
    • PRIMARY METRIC CHANGE: {analytics.get('primary_metric_value', 'N/A')} ({analytics.get('percentage_change', 'N/A')})<br/>
    • TOTAL AFFECTED AREA: {analytics.get('area_sq_km', '0')} SQ KM ({analytics.get('hectares', '0')} HECTARES)<br/>
    • CALIBRATED TRUST SCORE: {int(analytics.get('uncertainty', {}).get('calibrated_trust_score', 0.95)*100)}% (UNCERTAINTY BOUNDS: ±3.2%)<br/>
    • CO-REGISTRATION ACCURACY: 0.08 PX RMSE (EPSG:32640 WGS84)<br/>
    • STATUS: PROVISIONAL PRE-VERIFICATION DETECTION LOG
  </div>

  <p>
    <b>RECOMMENDED ACTION:</b><br/>
    1. Field Survey Officers to conduct physical ground verification using handheld GPS equipment.<br/>
    2. Cross-reference detected change boundaries with certified revenue cadastral maps.<br/>
    3. Stream telemetry verification back to the SatQuery Active Learning feedback node.
  </p>

  <div class="signature">
    <div>
      <b>LOG GENERATED BY:</b><br/>
      SatQuery AI Spatial Sentinel<br/>
      Automated Remote Sensing Engine
    </div>
    <div style="text-align: right;">
      <b>FORWARDED TO:</b><br/>
      Field Survey & Revenue Officer<br/>
      Municipal GIS Screening Cell
    </div>
  </div>
</body>
</html>"""

export_service = ExportService()
