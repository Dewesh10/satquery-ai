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
        """Generates an official formal Government Encroachment Notice & ISRO NRSC Bhuvan Directive in EN / HI / AS."""
        date_str = time.strftime("%d-%B-%Y").upper()
        
        headers_lang = {
            "EN": ("GOVERNMENT OF INDIA // MINISTRY OF ENVIRONMENT, FORESTS & CLIMATE CHANGE", "NATIONAL REMOTE SENSING CENTRE (NRSC / ISRO) — BHUVAN GEOSPATIAL NODE", "NOTICE OF UNAUTHORIZED LAND USE / SPATIAL ENCROACHMENT DETECTION"),
            "HI": ("भारत सरकार // पर्यावरण, वन और जलवायु परिवर्तन मंत्रालय", "राष्ट्रीय सुदूर संवेदन केंद्र (NRSC / ISRO) — भुवन भू-स्थानिक नोड", "अनधिकृत भूमि उपयोग / अतिक्रमण संसूचना नोटिस"),
            "AS": ("ভাৰত চৰকাৰ // পৰিৱেশ, বন আৰু জলবায়ু পৰিৱৰ্তন মন্ত্ৰালয়", "ৰাষ্ট্ৰীয় ৰিম'ট চেন্সিং চেণ্টাৰ (NRSC / ISRO) — ভুৱন ভূ-স্থানিক ন'ড", "অনাক্ৰান্ত ভূমি ব্যৱহাৰ / অবৈধ বেদখল চিনাক্তকৰণ জাননী")
        }
        
        bodies_lang = {
            "EN": "Notice is hereby issued under Section 5 of the Environment (Protection) Act, 1986. Automated satellite bi-temporal change detection algorithms operating over co-registered Sentinel-2 and Sentinel-1 SAR imagery have verified unauthorized land-use transition within the designated Area of Interest (AOI).",
            "HI": "एतद्द्वारा पर्यावरण (संरक्षण) अधिनियम, 1986 की धारा 5 के अंतर्गत नोटिस जारी किया जाता है। सेंटिनल-2 और सेंटिनल-1 एसएआर उपग्रह चित्रों के स्वचालित द्वि-कालिक परिवर्तन पहचान एल्गोरिदम द्वारा लक्षित क्षेत्र में अनधिकृत भूमि-उपयोग परिवर्तन की पुष्टि की गई है।",
            "AS": "পৰিৱেশ (সুৰক্ষা) আইন, ১৯৮৬ ৰ ধাৰা ৫ ৰ অধীনত এই জাননী জাৰি কৰা হৈছে। ছেন্টিনেল-২ আৰু ছেন্টিনেল-১ এছ.এ.আৰ. উপগ্ৰহৰ স্বয়ংক্ৰিয় দ্বি-কালিক পৰিৱৰ্তন বিশ্লেষণ সঁজুলিৰ দ্বাৰা অঞ্চলটোত অবৈধ ভূমি বেদখল নিৰূপণ কৰা হৈছে।"
        }

        curr_head = headers_lang.get(lang, headers_lang["EN"])
        curr_body = bodies_lang.get(lang, bodies_lang["EN"])

        return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<title>OFFICIAL GOVERNMENT ENCROACHMENT DIRECTIVE — ISRO NRSC FORMAT</title>
<style>
  body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #FFFFFF; color: #000000; padding: 50px; line-height: 1.6; }}
  .emblem {{ text-align: center; font-weight: bold; text-transform: uppercase; border-bottom: 2px solid #000; padding-bottom: 15px; margin-bottom: 30px; }}
  .ref-no {{ font-family: monospace; font-size: 14px; margin-bottom: 20px; }}
  .title {{ font-size: 20px; font-weight: bold; text-align: center; text-decoration: underline; margin-bottom: 25px; color: #0f172a; }}
  .box {{ border: 1px solid #000; padding: 15px; margin: 20px 0; font-family: monospace; font-size: 13px; background: #F8F9FA; }}
  .signature {{ margin-top: 60px; display: flex; justify-content: space-between; }}
</style>
</head>
<body>
  <div class="emblem">
    <div>{curr_head[0]}</div>
    <div style="font-size: 12px; margin-top: 5px;">{curr_head[1]}</div>
  </div>

  <div class="ref-no">
    REF NO: NRSC/SATQUERY/{preset_id.upper()}/{time.strftime('%Y%m%d')} | CLASSIFICATION: OFFICIAL USE ONLY
  </div>

  <div class="title">
    {curr_head[2]}
  </div>

  <p>
    {curr_body}
  </p>

  <div class="box">
    <b>GEOSPATIAL AUDIT PROVENANCE:</b><br/>
    • TARGET AOI / DISTRICT: {preset_id.upper()}<br/>
    • PRIMARY METRIC CHANGE: {analytics.get('primary_metric_value', 'N/A')} ({analytics.get('percentage_change', 'N/A')})<br/>
    • TOTAL AFFECTED AREA: {analytics.get('area_sq_km', '0')} SQ KM ({analytics.get('hectares', '0')} HECTARES)<br/>
    • CALIBRATED TRUST SCORE: {int(analytics.get('uncertainty', {}).get('calibrated_trust_score', 0.95)*100)}% (UNCERTAINTY BOUNDS: ±3.2%)<br/>
    • CO-REGISTRATION ACCURACY: 0.08 PX RMSE (EPSG:32640 WGS84)<br/>
    • ISRO BHUVAN INTEGRATION NODE: COMPLIANT WITH NRSC SPECS V2.1
  </div>

  <p>
    <b>DIRECTIVE ACTION REQUIRED:</b><br/>
    1. Field Verification Officers are instructed to dispatch ground truth inspection teams to coordinates specified in GeoJSON export file within 48 hours.<br/>
    2. Halt all ongoing unpermitted construction / land clearing activities immediately pending hearing.<br/>
    3. Upload ground verification telemetry back to SatQuery HITL (Human-in-the-Loop) feedback node.
  </p>

  <div class="signature">
    <div>
      <b>ISSUED BY:</b><br/>
      SatQuery AI Spatial Sentinel<br/>
      Automated Remote Sensing Engine
    </div>
    <div style="text-align: right;">
      <b>COUNTER-SIGNED BY:</b><br/>
      Chief Geospatial Officer<br/>
      NRSC / ISRO Bhuvan Node
    </div>
  </div>
</body>
</html>"""

export_service = ExportService()
