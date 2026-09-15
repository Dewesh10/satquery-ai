import React, { useState } from 'react';
import { Bell, ShieldAlert, X, Plus, Clock, Radio, CheckCircle2, AlertTriangle } from 'lucide-react';

interface SentinelMonitoringModalProps {
  currentPreset: string;
  onClose: () => void;
}

export const SentinelMonitoringModal: React.FC<SentinelMonitoringModalProps> = ({ currentPreset, onClose }) => {
  const [watchlists, setWatchlists] = useState([
    {
      id: "AOI-WATCH-01",
      name: "Jebel Ali Coastal Construction Watch",
      preset_id: "dubai_urban",
      schedule: "Every 6 Hours (Sentinel-2 Pass)",
      status: "ACTIVE_MONITORING",
      last_run: "2024-02-20T06:00:00Z",
      threshold: "> 5.0 sq km change",
      alert: {
        severity: "CRITICAL",
        title: "Unauthorized Construction Growth Detected",
        delta: "+18.4 sq km",
        time: "12 mins ago",
        message: "Encroachment threshold breached in Jebel Ali maritime corridor (+18.4 sq km growth)."
      }
    },
    {
      id: "AOI-WATCH-02",
      name: "Brahmaputra Flood Plain Sentinel",
      preset_id: "assam_flood",
      schedule: "Every 12 Hours (Sentinel-1 SAR Radar)",
      status: "ACTIVE_MONITORING",
      last_run: "2023-07-18T12:00:00Z",
      threshold: "> 10.0 sq km inundation",
      alert: {
        severity: "EMERGENCY",
        title: "Monsoon Flood Inundation Spike",
        delta: "+114.6 sq km submerged",
        time: "45 mins ago",
        message: "Submerged agricultural land spiked by +310.5%. Emergency evacuation protocol advised."
      }
    }
  ]);

  const [newWatchName, setNewWatchName] = useState("");
  const [thresholdInput, setThresholdInput] = useState("> 2.0 sq km change");

  const handleAddWatch = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newWatchName.trim()) return;
    setWatchlists([
      ...watchlists,
      {
        id: `AOI-WATCH-0${watchlists.length + 1}`,
        name: newWatchName,
        preset_id: currentPreset,
        schedule: "Every 6 Hours (Automatic Satellite Orbit Pass)",
        status: "ACTIVE_MONITORING",
        last_run: "Just Now",
        threshold: thresholdInput,
        alert: null
      }
    ]);
    setNewWatchName("");
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/85 backdrop-blur-md flex items-center justify-center p-4 font-mono select-none">
      <div className="w-full max-w-3xl bg-[#0A101D] border border-cyber-magenta rounded-xl shadow-magenta-glow p-6 relative space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-cyber-border pb-3">
          <div className="flex items-center gap-2">
            <Bell className="w-5 h-5 text-cyber-magenta animate-bounce" />
            <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wider">
              AUTONOMOUS SENTINEL MONITORING & ALERTING SYSTEM
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form to Pin Current AOI for Autonomous Watch */}
        <form onSubmit={handleAddWatch} className="p-4 bg-[#050811] rounded-lg border border-cyber-border space-y-3">
          <div className="text-xs font-bold text-cyber-magenta flex items-center gap-1.5 uppercase">
            <Plus className="w-4 h-4" /> PIN CURRENT AOI FOR AUTONOMOUS PASS MONITORING
          </div>
          <div className="grid grid-cols-3 gap-2">
            <input
              type="text"
              placeholder="Watchlist Name (e.g. Illegal Mining Watch)..."
              value={newWatchName}
              onChange={(e) => setNewWatchName(e.target.value)}
              className="col-span-2 bg-[#0A101D] border border-cyber-border rounded p-2 text-xs text-slate-100 placeholder-slate-500 focus:border-cyber-magenta focus:outline-none"
            />
            <button
              type="submit"
              className="px-3 py-2 bg-cyber-magenta text-white font-bold text-xs rounded hover:bg-magenta-600 transition shadow-magenta-glow flex items-center justify-center gap-1.5"
            >
              <Radio className="w-3.5 h-3.5" /> PIN WATCHLIST
            </button>
          </div>
        </form>

        {/* Active Pinned Watchlists & Real-time Alerts */}
        <div className="space-y-3">
          <div className="text-xs font-bold text-slate-400 uppercase tracking-wider">
            ACTIVE PINNED WATCHLISTS ({watchlists.length})
          </div>

          {watchlists.map((w) => (
            <div key={w.id} className="p-4 rounded-lg bg-[#050811] border border-slate-800 space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Radio className="w-4 h-4 text-cyber-emerald animate-pulse" />
                  <span className="font-bold text-xs text-slate-200">{w.name}</span>
                </div>
                <span className="text-[10px] font-mono text-cyber-cyan bg-cyber-cyan/10 border border-cyber-cyan/30 px-2 py-0.5 rounded">
                  {w.schedule}
                </span>
              </div>

              {/* Alert Push Notification Card if present */}
              {w.alert ? (
                <div className="p-3 rounded bg-red-950/40 border border-red-500/50 space-y-1 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-red-400 flex items-center gap-1.5">
                      <AlertTriangle className="w-4 h-4 text-red-400 animate-ping" />
                      {w.alert.severity}: {w.alert.title}
                    </span>
                    <span className="text-[10px] text-slate-400">{w.alert.time}</span>
                  </div>
                  <div className="text-slate-300 text-[11px]">{w.alert.message}</div>
                </div>
              ) : (
                <div className="text-[11px] text-slate-500 flex items-center gap-1">
                  <CheckCircle2 className="w-3.5 h-3.5 text-cyber-emerald" />
                  <span>No change threshold breach detected on last orbit pass.</span>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
