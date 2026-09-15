import React from 'react';
import { X, FileCode, FileSpreadsheet, FileText, Download, Building } from 'lucide-react';
import { AnalyticsData } from '../../types';

interface ExportModalProps {
  analytics: AnalyticsData | null;
  selectedPreset: string;
  onClose: () => void;
}

export const ExportModal: React.FC<ExportModalProps> = ({ analytics, selectedPreset, onClose }) => {
  if (!analytics) return null;

  const downloadGeoJSON = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(analytics.geojson, null, 2));
    const dlAnchor = document.createElement('a');
    dlAnchor.setAttribute("href", dataStr);
    dlAnchor.setAttribute("download", `satquery_${selectedPreset}.geojson`);
    document.body.appendChild(dlAnchor);
    dlAnchor.click();
    dlAnchor.remove();
  };

  const downloadCSV = () => {
    const csvContent = [
      "Metric,Value",
      `Preset ID,${analytics.preset_id}`,
      `Time Span,${analytics.time_span}`,
      `Primary Metric,${analytics.primary_metric_label}`,
      `Primary Value,${analytics.primary_metric_value}`,
      `Percentage Change,${analytics.percentage_change}`,
      `Area Sq Km,${analytics.area_sq_km}`,
      `Confidence,${analytics.confidence_score}`
    ].join("\n");

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", `satquery_metrics_${selectedPreset}.csv`);
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  const openPDFReport = () => {
    window.open(`http://localhost:8000/api/export/pdf?preset_id=${selectedPreset}`, '_blank');
  };

  const openGovernmentNotice = () => {
    window.open(`http://localhost:8000/api/export/government-notice?preset_id=${selectedPreset}`, '_blank');
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-4 select-none font-mono">
      <div className="w-full max-w-lg bg-[#0A101D] border border-cyber-border rounded-xl shadow-2xl p-6 relative space-y-5">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1 rounded text-slate-400 hover:text-white hover:bg-slate-800 transition"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Modal Title */}
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <Download className="w-5 h-5 text-cyber-cyan" />
            <h3 className="text-base font-bold text-slate-100 uppercase tracking-wider">
              EXPORT GEOSPATIAL ANALYSIS ARTIFACTS
            </h3>
          </div>
          <p className="text-xs text-slate-400">
            Export verified satellite vector maps, metrics, or government directives.
          </p>
        </div>

        {/* Export Options Grid */}
        <div className="space-y-3">
          {/* Option 1: Provisional Screening Log */}
          <div className="p-3.5 rounded-lg bg-[#050811] border border-blue-400/40 hover:border-blue-400 transition flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded bg-blue-500/10 border border-blue-400/40 text-blue-400">
                <Building className="w-5 h-5" />
              </div>
              <div>
                <div className="text-xs font-bold text-slate-200">Provisional Screening Log</div>
                <div className="text-[10px] text-slate-400">Pre-verification internal screening alert log</div>
              </div>
            </div>
            <button
              onClick={openGovernmentNotice}
              className="px-3 py-1.5 rounded bg-blue-500 text-white font-bold text-xs hover:bg-blue-600 transition"
            >
              PREVIEW LOG
            </button>
          </div>

          {/* Option 2: GeoJSON */}
          <div className="p-3.5 rounded-lg bg-[#050811] border border-cyber-cyan/30 hover:border-cyber-cyan transition flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded bg-cyber-cyan/10 border border-cyber-cyan/40 text-cyber-cyan">
                <FileCode className="w-5 h-5" />
              </div>
              <div>
                <div className="text-xs font-bold text-slate-200">GeoJSON Vector Polygons</div>
                <div className="text-[10px] text-slate-400">QGIS / ArcGIS compatible change boundaries</div>
              </div>
            </div>
            <button
              onClick={downloadGeoJSON}
              className="px-3 py-1.5 rounded bg-cyber-cyan text-black font-bold text-xs hover:bg-cyan-300 transition"
            >
              DOWNLOAD
            </button>
          </div>

          {/* Option 3: CSV */}
          <div className="p-3.5 rounded-lg bg-[#050811] border border-cyber-amber/30 hover:border-cyber-amber transition flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded bg-cyber-amber/10 border border-cyber-amber/40 text-cyber-amber">
                <FileSpreadsheet className="w-5 h-5" />
              </div>
              <div>
                <div className="text-xs font-bold text-slate-200">CSV Quantitative Metrics</div>
                <div className="text-[10px] text-slate-400">Tabular area stats & uncertainty bounds</div>
              </div>
            </div>
            <button
              onClick={downloadCSV}
              className="px-3 py-1.5 rounded bg-cyber-amber text-black font-bold text-xs hover:bg-amber-300 transition"
            >
              DOWNLOAD
            </button>
          </div>

          {/* Option 4: Executive PDF Report */}
          <div className="p-3.5 rounded-lg bg-[#050811] border border-cyber-emerald/30 hover:border-cyber-emerald transition flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded bg-cyber-emerald/10 border border-cyber-emerald/40 text-cyber-emerald">
                <FileText className="w-5 h-5" />
              </div>
              <div>
                <div className="text-xs font-bold text-slate-200">Executive PDF Analysis Report</div>
                <div className="text-[10px] text-slate-400">Print-ready executive report with grounded chips</div>
              </div>
            </div>
            <button
              onClick={openPDFReport}
              className="px-3 py-1.5 rounded bg-cyber-emerald text-black font-bold text-xs hover:bg-emerald-300 transition"
            >
              PRINT / SAVE
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
