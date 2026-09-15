import React from 'react';
import { Database, X, ShieldCheck, FileText, Globe, Award } from 'lucide-react';

interface DataLicensingModalProps {
  onClose: () => void;
}

export const DataLicensingModal: React.FC<DataLicensingModalProps> = ({ onClose }) => {
  return (
    <div className="fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-4 font-sans select-none">
      <div className="w-full max-w-2xl bg-[#0B132B] border border-cyber-cyan rounded-xl shadow-2xl p-6 relative space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-cyber-border pb-3">
          <div className="flex items-center gap-2">
            <Database className="w-5 h-5 text-cyber-cyan animate-pulse" />
            <h3 className="font-display font-bold text-sm text-slate-100 uppercase tracking-wider">
              SATELLITE DATA SOURCES, PROVENANCE & LICENSING DISCLOSURES
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Data Sources Grid */}
        <div className="space-y-3 font-mono text-xs">
          {/* ESA Copernicus */}
          <div className="p-3.5 bg-[#030712] border border-cyan-500/30 rounded-xl space-y-1">
            <div className="flex justify-between font-bold text-cyber-cyan">
              <span>ESA COPERNICUS SENTINEL-1 & SENTINEL-2</span>
              <span className="text-emerald-400 text-[10px] bg-emerald-500/10 px-2 py-0.5 rounded">OPEN ACCESS / CC-BY 4.0</span>
            </div>
            <div className="text-[11px] text-slate-300">Provider: European Space Agency (ESA) / EU Copernicus Open Access Hub</div>
            <div className="text-[10px] text-slate-400">Resolution: 10m GSD Optical MSI & Sentinel-1 C-Band SAR Radar</div>
          </div>

          {/* USGS Landsat */}
          <div className="p-3.5 bg-[#030712] border border-amber-500/30 rounded-xl space-y-1">
            <div className="flex justify-between font-bold text-amber-400">
              <span>USGS / NASA LANDSAT-8 & LANDSAT-9</span>
              <span className="text-emerald-400 text-[10px] bg-emerald-500/10 px-2 py-0.5 rounded">PUBLIC DOMAIN / UNRESTRICTED</span>
            </div>
            <div className="text-[11px] text-slate-300">Provider: United States Geological Survey (USGS) & NASA Goddard</div>
            <div className="text-[10px] text-slate-400">Resolution: 30m GSD OLI-2 Operational Land Imager</div>
          </div>

          {/* ISRO Bhuvan */}
          <div className="p-3.5 bg-[#030712] border border-blue-400/30 rounded-xl space-y-1">
            <div className="flex justify-between font-bold text-blue-400">
              <span>ISRO NRSC BHUVAN / IN-SPACe GEOSPATIAL NODE</span>
              <span className="text-blue-400 text-[10px] bg-blue-500/10 px-2 py-0.5 rounded">NATIONAL SPATIAL DATA LICENSE</span>
            </div>
            <div className="text-[11px] text-slate-300">Provider: National Remote Sensing Centre (NRSC / ISRO)</div>
            <div className="text-[10px] text-slate-400">Compliance: Indian Spatial Infrastructure Directives v2.1</div>
          </div>

          {/* Capella SAR */}
          <div className="p-3.5 bg-[#030712] border border-rose-500/30 rounded-xl space-y-1">
            <div className="flex justify-between font-bold text-rose-400">
              <span>CAPELLA SPACE HIGH-RES SAR SPOTLIGHT</span>
              <span className="text-amber-400 text-[10px] bg-amber-500/10 px-2 py-0.5 rounded">COMMERCIAL OPEN DATA PROGRAM</span>
            </div>
            <div className="text-[11px] text-slate-300">Provider: Capella Space Commercial Constellation</div>
            <div className="text-[10px] text-slate-400">Resolution: 0.5m High-Resolution Sub-Meter X-Band SAR</div>
          </div>
        </div>
      </div>
    </div>
  );
};
