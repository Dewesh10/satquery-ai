import React, { useState, useEffect } from 'react';
import { Bell, Radio, ShieldAlert, Clock, CheckCircle2, AlertTriangle, Send, Link, Activity } from 'lucide-react';

export const SentinelWatchtower: React.FC = () => {
  const [countdown, setCountdown] = useState(15138); // seconds to next pass
  const [webhookUrl, setWebhookUrl] = useState('https://api.disaster-management.gov.in/webhooks/sentinel');
  const [webhooks, setWebhooks] = useState<any[]>([
    {
      webhook_id: "WHK-001",
      url: "https://api.disaster-management.gov.in/webhooks/sentinel",
      min_severity: "CRITICAL",
      status: "HEALTHY",
      last_dispatch: "2024-02-20T06:40:22Z"
    }
  ]);
  const [alertLogs, setAlertLogs] = useState<any[]>([]);
  const [isTriggering, setIsTriggering] = useState(false);
  const [latestDispatchPayload, setLatestDispatchPayload] = useState<any | null>(null);

  useEffect(() => {
    const timer = setInterval(() => {
      setCountdown(prev => (prev > 0 ? prev - 1 : 15138));
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const formatTime = (secs: number) => {
    const hrs = Math.floor(secs / 3600);
    const mins = Math.floor((secs % 3600) / 60);
    const s = secs % 60;
    return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  const handleRegisterWebhook = async () => {
    if (!webhookUrl.trim()) return;
    try {
      const res = await fetch('http://localhost:8000/api/sentinel/webhooks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: webhookUrl, min_severity: 'WARNING' })
      });
      if (res.ok) {
        const data = await res.json();
        setWebhooks(prev => [...prev, data]);
        alert(`Webhook successfully registered! ID: ${data.webhook_id}`);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleTriggerSimulatedAlert = async () => {
    setIsTriggering(true);
    try {
      const res = await fetch('http://localhost:8000/api/sentinel/alerts/trigger', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          watchlist_id: 'AOI-WATCH-02',
          severity: 'CRITICAL',
          custom_message: 'Emergency threshold breach: Inundation spiked by +114.6 sq km across Brahmaputra basin.'
        })
      });
      if (res.ok) {
        const data = await res.json();
        setAlertLogs(prev => [data.alert, ...prev]);
        setLatestDispatchPayload(data);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsTriggering(false);
    }
  };

  return (
    <div className="w-full h-full bg-[#030712] p-6 overflow-y-auto space-y-6 font-sans select-none">
      {/* Studio Header */}
      <div className="flex items-center justify-between border-b border-cyber-border pb-4">
        <div>
          <div className="flex items-center gap-2">
            <Bell className="w-6 h-6 text-rose-500 animate-bounce" />
            <h2 className="font-display font-extrabold text-xl text-slate-100 uppercase tracking-wider">
              AUTONOMOUS SENTINEL ORBIT WATCHTOWER
            </h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            24/7 continuous autonomous satellite pass monitor with webhook alert notifications.
          </p>
        </div>

        {/* Orbit Pass Countdown & Action Buttons */}
        <div className="flex items-center gap-4">
          <button
            onClick={handleTriggerSimulatedAlert}
            disabled={isTriggering}
            className="px-4 py-2 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-mono font-bold text-xs flex items-center gap-2 transition shadow-lg shadow-rose-950/50"
          >
            <Send className="w-4 h-4" />
            <span>{isTriggering ? 'TRIGGERING...' : 'SIMULATE SATELLITE ALERT'}</span>
          </button>

          <div className="flex items-center gap-3 p-3 bg-[#0B132B] border border-rose-500/40 rounded-xl shadow-rose-950/40 shadow-xl">
            <Clock className="w-5 h-5 text-rose-400 animate-spin" />
            <div>
              <div className="text-[10px] font-mono text-slate-400">NEXT SENTINEL-2B ORBIT PASS</div>
              <div className="text-lg font-mono font-bold text-rose-400">{formatTime(countdown)}</div>
            </div>
          </div>
        </div>
      </div>

      {/* Webhook Configuration & Live Alert Logs */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Webhook Dispatch Engine */}
        <div className="p-6 rounded-2xl bg-[#0B132B]/90 border border-cyber-border space-y-4 backdrop-blur-xl shadow-2xl">
          <div className="flex items-center justify-between">
            <span className="font-display font-bold text-sm text-slate-100 uppercase flex items-center gap-2">
              <Link className="w-4 h-4 text-cyber-cyan" />
              REGISTERED EMERGENCY WEBHOOK ENDPOINTS
            </span>
          </div>

          <div className="flex items-center gap-2">
            <input
              type="text"
              value={webhookUrl}
              onChange={e => setWebhookUrl(e.target.value)}
              placeholder="https://your-domain.gov/webhooks/sentinel"
              className="flex-1 bg-[#030712] border border-slate-700 rounded-lg px-3 py-2 text-xs font-mono text-slate-200 focus:outline-none focus:border-cyber-cyan"
            />
            <button
              onClick={handleRegisterWebhook}
              className="px-3 py-2 rounded-lg bg-cyber-cyan text-black font-mono font-bold text-xs hover:bg-cyan-300 transition"
            >
              ADD WEBHOOK
            </button>
          </div>

          <div className="space-y-2.5 font-mono text-xs">
            {webhooks.map((wh, idx) => (
              <div key={idx} className="p-3.5 rounded-xl bg-[#030712] border border-slate-800 flex items-center justify-between">
                <div>
                  <div className="font-bold text-slate-200">{wh.webhook_id} — {wh.url}</div>
                  <div className="text-[10px] text-slate-400">Min Severity: {wh.min_severity} • Status: {wh.status}</div>
                </div>
                <span className="px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-[10px] font-bold">
                  ACTIVE
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Live Dispatched Payload Inspector */}
        <div className="p-6 rounded-2xl bg-[#0B132B]/90 border border-cyber-border space-y-4 backdrop-blur-xl shadow-2xl">
          <span className="font-display font-bold text-sm text-slate-100 uppercase flex items-center gap-2">
            <Activity className="w-4 h-4 text-rose-400" />
            LIVE DISPATCHED WEBHOOK PAYLOAD INSPECTOR
          </span>

          {latestDispatchPayload ? (
            <div className="p-4 rounded-xl bg-[#030712] border border-rose-500/40 font-mono text-xs space-y-2 overflow-x-auto">
              <div className="text-emerald-400 font-bold">HTTP 200 OK — WEBHOOK DISPATCH SUCCESS</div>
              <pre className="text-[11px] text-slate-300">
                {JSON.stringify(latestDispatchPayload, null, 2)}
              </pre>
            </div>
          ) : (
            <div className="p-6 rounded-xl bg-[#030712] border border-slate-800 text-center font-mono text-xs text-slate-500">
              Click 'SIMULATE SATELLITE ALERT' above to trigger an automated orbit pass breach and inspect the JSON webhook payload.
            </div>
          )}
        </div>
      </div>

      {/* Watchlist Stream Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="p-6 rounded-2xl bg-[#0B132B]/90 border border-cyber-border space-y-4 backdrop-blur-xl shadow-2xl">
          <div className="flex items-center justify-between">
            <span className="font-display font-bold text-sm text-slate-100 uppercase flex items-center gap-2">
              <Radio className="w-4 h-4 text-emerald-400 animate-pulse" />
              PINNED SURVEILLANCE WATCHLISTS (2 ACTIVE)
            </span>
          </div>

          <div className="space-y-3 font-mono text-xs">
            {alertLogs.map((alt, idx) => (
              <div key={idx} className="p-4 rounded-xl bg-[#030712] border border-rose-500/60 space-y-2">
                <div className="flex justify-between font-bold text-rose-400">
                  <span>{alt.title}</span>
                  <span className="text-[10px] bg-rose-500/10 border border-rose-500/30 px-2 py-0.5 rounded">{alt.severity}</span>
                </div>
                <div className="text-[11px] text-slate-300">{alt.message}</div>
              </div>
            ))}

            <div className="p-4 rounded-xl bg-[#030712] border border-rose-500/40 space-y-2">
              <div className="flex justify-between font-bold text-rose-400">
                <span>Jebel Ali Coastal Watch</span>
                <span className="text-[10px] bg-rose-500/10 border border-rose-500/30 px-2 py-0.5 rounded">CRITICAL BREACH</span>
              </div>
              <div className="text-[11px] text-slate-300">Target AOI: Dubai Coastal Sector 4 • Schedule: Every 6 Hours</div>
              <div className="text-[11px] text-rose-400 bg-rose-950/40 p-2.5 rounded border border-rose-500/30">
                ALERT: Unauthorized construction breached +5.0 sq km limit (+18.4 sq km detected).
              </div>
            </div>

            <div className="p-4 rounded-xl bg-[#030712] border border-cyan-500/40 space-y-2">
              <div className="flex justify-between font-bold text-cyber-cyan">
                <span>Brahmaputra Flood Plain Watch</span>
                <span className="text-[10px] bg-cyan-500/10 border border-cyan-500/30 px-2 py-0.5 rounded">ACTIVE PATROL</span>
              </div>
              <div className="text-[11px] text-slate-300">Target AOI: Assam Brahmaputra • Schedule: Every 12 Hours (SAR Radar)</div>
              <div className="text-[11px] text-emerald-400 flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4" />
                <span>Last orbit pass clear. Water margin within baseline thresholds.</span>
              </div>
            </div>
          </div>
        </div>

        {/* Orbit Satellite Fleet Status */}
        <div className="p-6 rounded-2xl bg-[#0B132B]/90 border border-cyber-border space-y-4 backdrop-blur-xl shadow-2xl">
          <span className="font-display font-bold text-sm text-slate-100 uppercase">
            ORBITING SATELLITE FLEET STATUS
          </span>

          <div className="space-y-3 text-xs font-mono">
            {[
              { name: 'Sentinel-2A MSI', agency: 'ESA / EU Copernicus', status: 'HEALTHY', altitude: '786 km' },
              { name: 'Sentinel-2B MSI', agency: 'ESA / EU Copernicus', status: 'HEALTHY', altitude: '786 km' },
              { name: 'Landsat-9 OLI-2', agency: 'NASA / USGS', status: 'HEALTHY', altitude: '705 km' },
              { name: 'Sentinel-1A SAR', agency: 'ESA Synthetic Radar', status: 'HEALTHY', altitude: '693 km' }
            ].map(sat => (
              <div key={sat.name} className="p-3.5 rounded-xl bg-[#030712] border border-slate-800 flex items-center justify-between">
                <div>
                  <div className="font-bold text-slate-200">{sat.name}</div>
                  <div className="text-[10px] text-slate-400">{sat.agency}</div>
                </div>
                <div className="text-right">
                  <div className="text-emerald-400 font-bold text-[10px]">{sat.status}</div>
                  <div className="text-slate-400 text-[10px]">{sat.altitude}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
