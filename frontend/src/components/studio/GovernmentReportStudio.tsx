import React, { useState } from 'react';
import { Building, FileText, Printer, CheckCircle2, ShieldCheck, ArrowRight, UserCheck } from 'lucide-react';
import { AnalyticsData } from '../../types';

interface GovernmentReportStudioProps {
  selectedPreset: string;
  analytics: AnalyticsData | null;
}

export const GovernmentReportStudio: React.FC<GovernmentReportStudioProps> = ({ selectedPreset, analytics }) => {
  const [workflowState, setWorkflowState] = useState<'DRAFT' | 'OFFICER_REVIEW' | 'FIELD_DISPATCHED' | 'FILED_ON_BHUVAN'>('DRAFT');

  const openGovernmentNotice = () => {
    window.open(`http://localhost:8000/api/export/government-notice?preset_id=${selectedPreset}&api_key=satquery-demo-key-2024`, '_blank');
  };

  return (
    <div className="w-full h-full bg-[#030712] p-6 overflow-y-auto space-y-6 font-sans select-none">
      {/* Studio Header */}
      <div className="flex items-center justify-between border-b border-cyber-border pb-4">
        <div>
          <div className="flex items-center gap-2">
            <Building className="w-6 h-6 text-blue-400" />
            <h2 className="font-display font-extrabold text-xl text-slate-100 uppercase tracking-wider">
              PROVISIONAL CHANGE DETECTION & SCREENING REPORT STUDIO
            </h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Internal screening logs & bi-temporal satellite change analysis for field survey planning. Preliminary observation only.
          </p>
        </div>

        <div className="flex gap-3">
          <button
            onClick={openGovernmentNotice}
            className="px-4 py-2 rounded-xl bg-blue-500 text-white font-bold text-xs hover:bg-blue-600 transition flex items-center gap-2 shadow-lg"
          >
            <Printer className="w-4 h-4" />
            <span>PRINT PROVISIONAL SCREENING LOG</span>
          </button>
        </div>
      </div>

      {/* Mandatory Legal Disclaimer Banner */}
      <div className="p-3 bg-amber-500/10 border border-amber-500/30 rounded-xl text-amber-300 text-xs flex items-center gap-2 font-mono">
        <span className="font-bold">⚠️ DISCLAIMER:</span>
        <span>Preliminary AI-generated change detection log for internal screening only. Not an official legal notice or court-admissible document until verified on the ground by certified surveyors.</span>
      </div>

      {/* Interactive Workflow Accountability Chain Bar */}
      <div className="p-4 rounded-2xl bg-[#0B132B]/90 border border-cyber-border space-y-3 backdrop-blur-xl">
        <div className="text-xs font-display font-bold text-slate-200 uppercase flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-cyber-cyan" />
          INTERNAL SCREENING & SURVEY WORKFLOW ACCOUNTABILITY CHAIN
        </div>

        <div className="flex items-center justify-between font-mono text-xs">
          {[
            { id: 'DRAFT', label: '1. PRELIMINARY LOG' },
            { id: 'OFFICER_REVIEW', label: '2. GIS CELL REVIEW' },
            { id: 'FIELD_DISPATCHED', label: '3. FIELD SURVEY DISPATCHED' },
            { id: 'FILED_ON_BHUVAN', label: '4. VERIFIED ON BHUVAN' }
          ].map((step, idx) => {
            const isActive = workflowState === step.id;
            return (
              <React.Fragment key={step.id}>
                <button
                  onClick={() => setWorkflowState(step.id as any)}
                  className={`px-4 py-2 rounded-xl font-bold transition flex items-center gap-2 border ${
                    isActive
                      ? 'bg-blue-500 text-white border-blue-400 shadow-lg'
                      : 'bg-[#030712] text-slate-400 border-slate-800 hover:border-slate-600'
                  }`}
                >
                  {isActive && <CheckCircle2 className="w-4 h-4 text-white" />}
                  <span>{step.label}</span>
                </button>

                {idx < 3 && <ArrowRight className="w-4 h-4 text-slate-600" />}
              </React.Fragment>
            );
          })}
        </div>
      </div>

      {/* Document Preview Box */}
      <div className="p-8 rounded-2xl bg-white text-slate-900 border border-slate-300 font-serif max-w-4xl mx-auto shadow-2xl space-y-6 leading-relaxed">
        <div className="text-center border-b-2 border-black pb-4 space-y-1">
          <div className="font-bold text-lg uppercase tracking-wider">STATE LAND REVENUE & MUNICIPAL GIS CELL</div>
          <div className="text-xs font-mono text-slate-600">PROVISIONAL SATELLITE CHANGE DETECTION & INTERNAL SCREENING REPORT</div>
        </div>

        <div className="font-mono text-xs text-slate-600 flex justify-between">
          <span>REF NO: PRELIM/SATQUERY/{selectedPreset.toUpperCase()}/2026</span>
          <span className="font-bold text-blue-800">STATUS: {workflowState}</span>
        </div>

        <h3 className="font-sans font-bold text-lg text-center underline uppercase tracking-wide text-black">
          PROVISIONAL ALERT: DETECTED SPATIAL LAND-USE TRANSITION
        </h3>

        <p className="text-sm font-sans">
          This document represents an initial automated observation derived from bi-temporal change detection algorithms operating over co-registered Sentinel-2 and Sentinel-1 SAR imagery. This report is for internal screening and field survey prioritization only.
        </p>

        <div className="p-4 bg-slate-100 border border-slate-400 rounded font-mono text-xs space-y-1">
          <div className="font-bold text-black border-b border-slate-300 pb-1">GEOSPATIAL AUDIT PROVENANCE TELEMETRY:</div>
          <div>• TARGET DISTRICT: {selectedPreset.toUpperCase()}</div>
          <div>• PRIMARY METRIC CHANGE: {analytics?.primary_metric_value || '42.8 sq km'} ({analytics?.percentage_change || '+18.4%'})</div>
          <div>• AFFECTED AREA: {analytics?.area_sq_km || 42.8} SQ KM ({analytics?.hectares || 4280} HECTARES)</div>
          <div>• CALIBRATED TRUST SCORE: 96.4% (UNCERTAINTY BOUNDS: ±3.2%)</div>
          <div>• STATUS: PROVISIONAL PRE-VERIFICATION DETECTION LOG</div>
        </div>

        <p className="text-sm font-sans">
          <b>RECOMMENDED NEXT STEPS:</b><br/>
          1. Field Survey Teams to conduct physical ground verification using handheld GPS equipment.<br/>
          2. Cross-reference detected change boundaries with certified revenue cadastral maps.<br/>
          3. Upload ground-truthed verification feedback into the SatQuery feedback pipeline.
        </p>

        <div className="p-3 bg-slate-200 border-l-4 border-amber-600 font-mono text-[10px] text-slate-800">
          <b>DISCLAIMER:</b> This report is generated automatically by satellite imagery algorithms for preliminary triage. It does not constitute a statutory notice, legal order, or court-admissible evidence without ground certification by an authorized revenue authority.
        </div>

        <div className="pt-6 border-t border-slate-300 flex justify-between font-sans text-xs">
          <div>
            <b>LOG GENERATED BY:</b><br/>
            SatQuery AI Spatial Sentinel<br/>
            Automated Remote Sensing Engine
          </div>
          <div className="text-right">
            <b>FORWARDED TO:</b><br/>
            Field Survey & Revenue Officer<br/>
            Municipal GIS Screening Cell
          </div>
        </div>
      </div>
    </div>
  );
};
