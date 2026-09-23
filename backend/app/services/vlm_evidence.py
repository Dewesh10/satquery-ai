from typing import Dict, List, Any
from app.core.config import settings
from app.core.data_store import data_store

class VLMEvidenceEngine:
    def synthesize_answer(self, prompt: str, preset_id: str, analytics: Dict[str, Any], lang: str = "EN") -> Dict[str, Any]:
        """Generates templated multilingual evidence summaries (EN, HI, AS) from preset spatial metadata."""
        
        scenes = data_store.search_scenes(preset_id=preset_id)
        scene_pre = scenes[0] if len(scenes) > 0 else {}
        scene_post = scenes[1] if len(scenes) > 1 else scenes[0]
        
        if preset_id == "newyork_urban":
            text_en = (
                "Bi-temporal satellite analysis between **April 10, 2018** and **April 15, 2024** "
                "identifies **54.2 sq km** of new urban construction and shoreline redevelopment across the New York Metropolitan area (+14.8% growth)."
            )
            text_hi = (
                "**10 अप्रैल, 2018** और **15 अप्रैल, 2024** के बीच उपग्रह विश्लेषण से "
                "न्यूयॉ़र्क महानगरीय क्षेत्र में **54.2 वर्ग किमी** नए शहरी निर्माण और तटवर्ती पुनर्विकास की पुष्टि हुई है।"
            )
            text_as = (
                "**১০ এপ্ৰিল, ২০১৮** আৰু **১৫ এপ্ৰিল, ২০২৪** ৰ ভিতৰত উপগ্ৰহ বিশ্লেষণে "
                "নিউয়ৰ্ক মহানগৰ অঞ্চলত **৫৪.২ বৰ্গ কিমি** নতুন নগৰ নিৰ্মাণ চিহ্নিত কৰিছে।"
            )

        elif preset_id == "india_delhi":
            text_en = (
                "Multi-spectral satellite analysis over the National Capital Region (Delhi-Gurugram-Noida) between 2019 and 2024 "
                "maps **88.4 sq km** of cropland-to-built-up conversion (+28.6% expansion)."
            )
            text_hi = (
                "2019 और 2024 के बीच राष्ट्रीय राजधानी क्षेत्र (दिल्ली-गुरुग्राम-नोएडा) के उपग्रह विश्लेषण से "
                "**88.4 वर्ग किमी** कृषि भूमि के पक्के शहरी निर्माण में परिवर्तन का नक्शा तैयार किया गया है।"
            )
            text_as = (
                "২০১৯ আৰু ২০২৪ ৰ ভিতৰত ৰাষ্ট্ৰীয় ৰাজধানী অঞ্চল (দিল্লী-গুৰুগ্ৰাম-নয়ডা) ৰ উপগ্ৰহ বিশ্লেষণে "
                "**৮৮.৪ বৰ্গ কিমি** কৃষি ভূমি নগৰ নিৰ্মাণলৈ ৰূপান্তৰিত হোৱা দেখা গৈছে।"
            )

        elif preset_id == "india_mumbai":
            text_en = (
                "SAR radar and optical specular fusion over the Mumbai coast (2018-2024) "
                "verifies **24.6 sq km** of new coastal land reclamation and container terminal expansion."
            )
            text_hi = (
                "मुंबई तट (2018-2024) पर एसएआर रडार और ऑप्टिकल विश्लेषण से "
                "**24.6 वर्ग किमी** नए तटीय भूमि सुधार और बंदरगाह विस्तार की पुष्टि होती है।"
            )
            text_as = (
                "মুম্বাই উপকূলত (২০১৮-২০২৪) ৰাডাৰ আৰু অপটিকেল বিশ্লেষণে "
                "**২৪.৬ বৰ্গ কিমি** নতুন উপকূলীয় ভূ-পুনৰুদ্ধাৰ নিশ্চিত কৰে।"
            )

        elif preset_id == "dubai_urban":
            text_en = (
                "Based on bi-temporal satellite analysis between **March 15, 2018** and **February 20, 2024**, "
                "we observed significant urban built-up expansion in the Dubai coastal sector. "
                "The automated change detection pipeline identified **42.8 sq km** of new impervious surface growth (+18.4% increase)."
            )
            text_hi = (
                "**15 मार्च, 2018** और **20 फरवरी, 2024** के बीच उपग्रह विश्लेषण के आधार पर, "
                "हमने दुबई तटीय क्षेत्र में महत्वपूर्ण शहरी निर्माण विस्तार देखा है। "
                "स्वचालित परिवर्तन पहचान तंत्र ने **42.8 वर्ग किमी** नए पक्के निर्माण वृद्धि (+18.4% वृद्धि) की पहचान की है।"
            )
            text_as = (
                "**১৫ মাৰ্চ, ২০১৮** আৰু **২০ ফেব্ৰুৱাৰী, ২০২৪** ৰ মধ্যৱৰ্তী উপগ্ৰহ বিশ্লেষণৰ ভিত্তিত, "
                "আমি দুবাই উপকূলীয় অঞ্চলত গুৰুত্বপূৰ্ণ নগৰ নিৰ্মাণ সম্প্ৰসাৰণ লক্ষ্য কৰিছো। "
                "স্বয়ংক্ৰিয় পৰিৱৰ্তন চিনাক্তকৰণ প্ৰণালীয়ে **৪২.৮ বৰ্গ কিমি** নতুন নিৰ্মাণ বৃদ্ধি চিনাক্ত কৰিছে।"
            )

        elif preset_id == "assam_flood":
            text_en = (
                "Sentinel-1 C-band Synthetic Aperture Radar (SAR) backscatter analysis between May 10 and July 18, 2023 "
                "maps **114.6 sq km** of flood inundation across the Brahmaputra river basin. "
                "SAR VV co-polarization backscatter values dropped below **-22.4 dB**, confirming submerged cropland."
            )
            text_hi = (
                "10 मई और 18 जुलाई, 2023 के बीच सेंटिनल-1 सी-बैंड एसएआर रडार विश्लेषण ने "
                "ब्रह्मपुत्र नदी बेसिन में **114.6 वर्ग किमी** जलमग्न क्षेत्र का मानचित्रण किया है। "
                "जलमग्न कृषि भूमि की पुष्टि **-22.4 dB** से नीचे रडार बैकस्कैटर द्वारा की गई है।"
            )
            text_as = (
                "১০ মে’ আৰু ১৮ জুলাই, ২০২৩ ৰ ভিতৰত চেণ্টিনেল-১ এছ এ আৰ ৰাডাৰ বিশ্লেষণে "
                "ব্ৰহ্মপুত্ৰ নদী অৱবাহিকাত **১১৪.৬ বৰ্গ কিমি** প্লাৱিত অঞ্চল চিহ্নিত কৰিছে। "
                "জলমগ্ন কৃষি ভূমি **-২২.৪ dB** ৰ তলত ৰাডাৰ বেকস্কেটাৰৰ দ্বাৰা নিশ্চিত কৰা হৈছে।"
            )

        else:
            text_en = f"Satellite bi-temporal analysis confirms **{analytics.get('primary_metric_value', 'change')}** ({analytics.get('percentage_change', '0%')}) across target AOI."
            text_hi = f"उपग्रह विश्लेषण लक्ष्य क्षेत्र में **{analytics.get('primary_metric_value', 'परिवर्तन')}** ({analytics.get('percentage_change', '0%')}) की पुष्टि करता है।"
            text_as = f"উপগ্ৰহ বিশ্লেষণে লক্ষ্য স্থানত **{analytics.get('primary_metric_value', 'পৰিৱৰ্তন')}** ({analytics.get('percentage_change', '0%')}) নিশ্চিত কৰে।"

        selected_text = text_en
        if lang == "HI":
            selected_text = text_hi
        elif lang == "AS":
            selected_text = text_as

        evidence_cards = [
            {
                "id": "EVID-001",
                "title": f"Spatial Feature Evidence ({preset_id.upper()})",
                "scene_id": scene_post.get("id", "S2B_20240220"),
                "sensor": scene_post.get("sensor", "Sentinel-2B MSI"),
                "timestamp": scene_post.get("datetime", "2024-02-20"),
                "coordinates": scene_post.get("center", [25.08, 55.20]),
                "metric": analytics.get("primary_metric_value", "Change Detected"),
                "confidence": "N/A — Templated Summary",
                "thumbnail": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=400&q=80",
                "type": "CHANGE_HIGHLIGHT"
            }
        ]

        return {
            "answer": selected_text,
            "lang": lang,
            "provenance": {
                "scenes_referenced": [scene_pre.get("id"), scene_post.get("id")],
                "sensors": [scene_pre.get("sensor"), scene_post.get("sensor")],
                "timestamps": [scene_pre.get("datetime"), scene_post.get("datetime")],
                "verification_status": "TEMPLATED_SUMMARY"
            },
            "evidence_cards": evidence_cards
        }

vlm_engine = VLMEvidenceEngine()
