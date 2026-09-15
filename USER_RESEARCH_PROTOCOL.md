# SatQuery AI — User Research & Domain Feedback Protocol

> [!IMPORTANT]
> **Status**: Primary domain user research (interviews with State Land Revenue Officers, Municipal GIS Cell Analysts, and Environmental NGOs) has **not yet taken place**. This document provides the operational interview protocol and structured survey framework to guide these essential interactions.

---

## 1. Research Objectives

1. **Workflow Alignment**: Understand how revenue inspectors and municipal GIS teams currently discover, log, and verify land-use changes or illegal encroachments.
2. **Trust & Accuracy Requirements**: Determine acceptable false-positive vs. false-negative thresholds for automated satellite detection before a field inspector is dispatched.
3. **Legal & Administrative Constraints**: Identify the exact legal chain of custody required before a satellite-detected change can be converted into an official notice.
4. **Interface Preferences**: Test whether field officers prefer high-level executive summary dashboards, raw GIS vector layers (GeoJSON/SHP), or natural language copilot interaction.

---

## 2. Target Persona 1: State Land Revenue Officer (Tehsildar / Patwari / Revenue Inspector)

### Core Focus: Encroachment Detection, Cadastral Alignment & Legal Proceedings

#### Interview Questions:
1. **Current Process**: How does your office currently receive information about unauthorized land conversion (e.g., agricultural land converted to commercial built-up)?
2. **Field Verification**: When a satellite alert flags a potential encroachment, what specific evidence does a revenue inspector need to collect on the ground to issue a statutory show-cause notice?
3. **Cadastral Overlay**: How are satellite boundaries matched against government revenue maps (khasra / survey numbers)? What co-registration error margin is acceptable?
4. **False Positive Tolerance**: If SatQuery flags 10 potential encroachments and 3 turn out to be seasonal crop harvests, how does that affect your team's trust in the software?
5. **Report Format**: What specific fields MUST be present in an internal screening log before you assign a field inspector to visit the site?

---

## 3. Target Persona 2: Municipal GIS Cell Analyst (Urban Planning & Infrastructure)

### Core Focus: Rapid Urbanization, Wetland Encroachment & Asset Tracking

#### Interview Questions:
1. **Monitoring Cadence**: How often does your GIS cell currently update satellite imagery layers for municipal boundary monitoring (monthly, quarterly, annually)?
2. **Data Pipeline**: Do you currently ingest open STAC catalogs (Sentinel/Landsat) or rely on vendor-delivered pre-processed satellite rasters?
3. **Cloud Interference**: During monsoon seasons (heavy cloud cover), what is your protocol when optical imagery is unavailable for 4-8 consecutive weeks? Does SAR radar imagery fulfill your monitoring needs?
4. **Integration**: Would your team use SatQuery AI as a standalone web application, or do you require direct REST API / WMS / WFS integration into your existing ArcGIS / QGIS enterprise stack?

---

## 4. Target Persona 3: Environmental / Land Monitoring NGO Representative

### Core Focus: Deforestation, Coastal Degradation & Community Land Rights

#### Interview Questions:
1. **Public Verification**: What open data sources (e.g., CWC bulletins, USGS hydrometric gauges) do you rely on to independently verify satellite-based disaster or deforestation claims?
2. **Alert Thresholds**: What area threshold (e.g., 0.1 hectare vs. 5 hectares) is actionable for community monitoring and advocacy?
3. **Accessibility**: Is a multi-lingual natural language copilot (English, Hindi, Assamese) useful for non-technical community advocates operating in regional districts?

---

## 5. Problem-First Outreach Message Templates

### Template A: Outreach to Land Revenue / Survey Officers (Tehsildars / Patwaris)
**Subject**: *Quick question on how your revenue office screens unauthorized land conversion*

> Hi [Name],
> 
> I am conducting independent research on how state land revenue offices and survey inspectors currently prioritize physical ground inspections for unauthorized land conversions (e.g. cropland converted to unpermitted construction).
> 
> I’d love to learn from your experience — specifically:
> 1. How does your office currently spot unauthorized land-use changes before a physical inspection is assigned?
> 2. When satellite pre-screening is used, what single piece of information is most important to a field inspector (Khasra plot no, before/after photo, or plot area in hectares)?
> 
> Would you be open to a 20-minute call or answering 2 quick questions via email this week?
> 
> Best regards,  
> Dewesh  
> Open-Source Geospatial Developer (`github.com/Dewesh10/satquery-ai`)

---

### Template B: Outreach to Municipal GIS Cell Analysts
**Subject**: *Research on monsoon cloud cover protocols in municipal GIS monitoring*

> Hi [Name],
> 
> I noticed your work in urban spatial planning and wanted to ask a quick research question.
> 
> We are studying how municipal GIS cells handle satellite-based boundary monitoring during heavy monsoon cloud cover (when optical imagery is obstructed for 4-8 consecutive weeks).
> 
> Do your teams rely on synthetic aperture radar (SAR) passes during monsoons, or do you pause satellite monitoring until clear optical passes return?
> 
> If you have 20 minutes for a brief conversation, I’d be very grateful for your perspective on this workflow challenge.
> 
> Best,  
> Dewesh  
> `github.com/Dewesh10/satquery-ai` (MIT Licensed)

---

## 6. Feedback Logging & Action Plan

Upon conducting interviews, record responses using the following standardized feedback template:

```markdown
### Interview Log: [Date] — [Persona Role]
- **Organization / Location**: 
- **Key Pain Point Mentioned**: 
- **Feedback on $2.5\sigma$ Threshold**: 
- **Feedback on Report Format**: 
- **Actionable Feature Requests**: 
```
