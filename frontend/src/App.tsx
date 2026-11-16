import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { SatMapWorkspace } from './components/map/SatMapWorkspace';
import { SplitScreenSlider } from './components/map/SplitScreenSlider';
import { CopilotDrawer } from './components/copilot/CopilotDrawer';
import { EvidenceDrawer } from './components/evidence/EvidenceDrawer';
import { AnalyticsPanel } from './components/analytics/AnalyticsPanel';
import { TimeSlider } from './components/timeline/TimeSlider';
import { ExportModal } from './components/export/ExportModal';
import { PixelChipMagnifier } from './components/inspector/PixelChipMagnifier';
import { QueryHistoryModal } from './components/history/QueryHistoryModal';

import { ErrorBoundary } from './components/common/ErrorBoundary';

const BandMathStudio = React.lazy(() => import('./components/studio/BandMathStudio').then(m => ({ default: m.BandMathStudio })));
const DAGStudio = React.lazy(() => import('./components/studio/DAGStudio').then(m => ({ default: m.DAGStudio })));
const SentinelWatchtower = React.lazy(() => import('./components/studio/SentinelWatchtower').then(m => ({ default: m.SentinelWatchtower })));
const GovernmentReportStudio = React.lazy(() => import('./components/studio/GovernmentReportStudio').then(m => ({ default: m.GovernmentReportStudio })));
const HITLStudio = React.lazy(() => import('./components/studio/HITLStudio').then(m => ({ default: m.HITLStudio })));
const PipelineHealthStudio = React.lazy(() => import('./components/studio/PipelineHealthStudio').then(m => ({ default: m.PipelineHealthStudio })));
const DataLicensingModal = React.lazy(() => import('./components/licensing/DataLicensingModal').then(m => ({ default: m.DataLicensingModal })));
const ModelBenchmarkingModal = React.lazy(() => import('./components/benchmarking/ModelBenchmarkingModal').then(m => ({ default: m.ModelBenchmarkingModal })));
const SystemRoadmapModal = React.lazy(() => import('./components/roadmap/SystemRoadmapModal').then(m => ({ default: m.SystemRoadmapModal })));

import { PresetLocation, QueryPlan, AnalyticsData, EvidenceData, EvidenceCard } from './types';
import { fetchPresets, executeQuery } from './lib/api';
import { soundEngine } from './lib/sound';

export function App() {
  const [presets, setPresets] = useState<Record<string, PresetLocation>>({});
  const [selectedPresetId, setSelectedPresetId] = useState<string>('dubai_urban');
  const [activeLayer, setActiveLayer] = useState<string>('RGB');
  const [splitScreenMode, setSplitScreenMode] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<string>('WORKSPACE');
  const [selectedLang, setSelectedLang] = useState<string>('EN');
  
  // Drawer Collapse States
  const [leftCollapsed, setLeftCollapsed] = useState<boolean>(false);
  const [rightCollapsed, setRightCollapsed] = useState<boolean>(false);

  // Modals States
  const [isExportOpen, setIsExportOpen] = useState<boolean>(false);
  const [isLicensingOpen, setIsLicensingOpen] = useState<boolean>(false);
  const [isBenchmarkingOpen, setIsBenchmarkingOpen] = useState<boolean>(false);
  const [isRoadmapOpen, setIsRoadmapOpen] = useState<boolean>(false);
  const [isHistoryOpen, setIsHistoryOpen] = useState<boolean>(false);
  const [inspectedChip, setInspectedChip] = useState<EvidenceCard | null>(null);
  
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [activePlan, setActivePlan] = useState<QueryPlan | null>(null);
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [evidence, setEvidence] = useState<EvidenceData | null>(null);
  
  const [flyToCoords, setFlyToCoords] = useState<[number, number] | null>(null);
  const [aoiPolygon, setAoiPolygon] = useState<[number, number][] | null>(null);

  useEffect(() => {
    fetchPresets().then(res => {
      setPresets(res);
      handleExecuteQuery(res['dubai_urban'].suggested_prompt, 'dubai_urban', selectedLang);
    });
  }, []);

  const [customZonalStats, setCustomZonalStats] = useState<any | null>(null);

  const handleRunCustomAOI = async (poly: [number, number][]) => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/raster/zonal-stats', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-API-Key': 'satquery-demo-key-2024' },
        body: JSON.stringify({ coordinates: poly })
      });
      if (res.ok) {
        const stats = await res.json();
        setCustomZonalStats(stats);
        if (analytics) {
          setAnalytics({
            ...analytics,
            area_sq_km: stats.area_metrics.area_sq_km,
            hectares: stats.area_metrics.hectares,
            geojson: stats.geojson
          });
        }
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleSelectPreset = (presetId: string) => {
    setSelectedPresetId(presetId);
    setFlyToCoords(null);
    setAoiPolygon(null);
    setCustomZonalStats(null);
    const p = presets[presetId];
    if (p) {
      handleExecuteQuery(p.suggested_prompt, presetId, selectedLang);
    }
  };

  const handleChangeLang = (lang: string) => {
    setSelectedLang(lang);
    const p = presets[selectedPresetId];
    const prompt = p ? p.suggested_prompt : 'Show built-up growth';
    handleExecuteQuery(prompt, selectedPresetId, lang);
  };

  const handleExecuteQuery = async (prompt: string, presetId = selectedPresetId, lang = selectedLang) => {
    setIsProcessing(true);
    soundEngine.playQueryRun();
    try {
      const res = await executeQuery(prompt, presetId, lang);
      setActivePlan(res.plan);
      setAnalytics(res.analytics);
      setEvidence(res.evidence);
      if (res.plan && res.plan.selected_preset_id) {
        setSelectedPresetId(res.plan.selected_preset_id);
      }
      if (res.plan && res.plan.preset && res.plan.preset.center) {
        setFlyToCoords(res.plan.preset.center as [number, number]);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleReplayRun = (runData: any) => {
    if (runData.plan) setActivePlan(runData.plan);
    if (runData.analytics) setAnalytics(runData.analytics);
    if (runData.evidence) setEvidence(runData.evidence);
    if (runData.preset_id) {
      setSelectedPresetId(runData.preset_id);
      if (presets[runData.preset_id]?.center) {
        setFlyToCoords(presets[runData.preset_id].center as [number, number]);
      }
    }
    setActiveTab('WORKSPACE');
  };

  const currentPreset = presets[selectedPresetId] || {
    name: 'Satellite AOI',
    category: 'Analysis Preset',
    center: [25.08, 55.20],
    zoom: 12,
    bbox: [55.12, 24.95, 55.35, 25.15],
    dates: ['2018-03-15', '2024-02-20'],
    sensors: ['Sentinel-2A MSI', 'Sentinel-2B MSI'],
    suggested_prompt: 'Analyze change detection'
  };

  return (
    <div className="flex flex-col h-screen w-screen overflow-hidden bg-[#030712] font-sans antialiased text-slate-100">
      {/* Top Main Navigation Bar */}
      <Navbar
        presets={presets}
        selectedPreset={selectedPresetId}
        onSelectPreset={handleSelectPreset}
        activeLayer={activeLayer}
        onChangeLayer={setActiveLayer}
        splitScreenMode={splitScreenMode}
        onToggleSplitScreen={() => setSplitScreenMode(!splitScreenMode)}
        onOpenExport={() => setIsExportOpen(true)}
        onOpenBenchmarking={() => setIsBenchmarkingOpen(true)}
        onOpenRoadmap={() => setIsRoadmapOpen(true)}
        onOpenHistory={() => setIsHistoryOpen(true)}
        selectedLang={selectedLang}
        onChangeLang={handleChangeLang}
        activeTab={activeTab}
        onChangeTab={setActiveTab}
        isProcessing={isProcessing}
      />

      {/* Main Work Area Layout */}
      <div className="flex flex-1 overflow-hidden relative">
        <ErrorBoundary>
          {activeTab === 'WORKSPACE' && (
            <>
              {/* Left: Natural Language Copilot Drawer */}
              <CopilotDrawer
                currentPreset={currentPreset}
                onExecuteQuery={handleExecuteQuery}
                isProcessing={isProcessing}
                activePlan={activePlan}
                collapsed={leftCollapsed}
                onToggleCollapse={() => setLeftCollapsed(!leftCollapsed)}
              />

              {/* Center: 3D Satellite Map Canvas Workspace */}
              <div className="flex-1 relative h-full">
                {splitScreenMode ? (
                  <SplitScreenSlider preset={currentPreset} onClose={() => setSplitScreenMode(false)} />
                ) : (
                  <SatMapWorkspace
                    preset={currentPreset}
                    analytics={analytics}
                    activeLayer={activeLayer}
                    flyToCoords={flyToCoords}
                    aoiPolygon={aoiPolygon}
                    onDrawAOI={setAoiPolygon}
                    onRunCustomAOI={handleRunCustomAOI}
                  />
                )}

                {/* Data Sources & Licensing Badge */}
                <button
                  onClick={() => setIsLicensingOpen(true)}
                  className="absolute top-4 left-4 z-20 px-3 py-1.5 rounded-xl bg-[#0B132B]/85 border border-cyan-500/30 text-cyber-cyan text-xs font-mono font-bold hover:bg-cyan-500/10 transition backdrop-blur-md shadow-cyan-glow flex items-center gap-1.5"
                >
                  <span>🌐 SATELLITE DATA SOURCES & LICENSING</span>
                </button>

                {/* Bottom Floating Analytics Panel */}
                <AnalyticsPanel
                  analytics={analytics}
                  onOpenHITL={() => setActiveTab('HITL_STUDIO')}
                />

                {/* Time Slider Timeline Scrubber */}
                {!splitScreenMode && <TimeSlider preset={currentPreset} />}
              </div>

              {/* Right: Grounded Evidence Drawer */}
              <EvidenceDrawer
                evidence={evidence}
                presetId={selectedPresetId}
                onFlyToEvidence={(coords) => {
                  soundEngine.playMapFly();
                  setFlyToCoords(coords);
                }}
                onInspectChip={(card) => setInspectedChip(card)}
                collapsed={rightCollapsed}
                onToggleCollapse={() => setRightCollapsed(!rightCollapsed)}
              />
            </>
          )}

          <React.Suspense fallback={<div className="w-full h-full bg-[#030712] flex items-center justify-center font-mono text-xs text-cyber-cyan">LOADING STUDIO MODULE...</div>}>
            {activeTab === 'BAND_MATH' && <BandMathStudio />}
            {activeTab === 'DAG_STUDIO' && <DAGStudio plan={activePlan} />}
            {activeTab === 'PIPELINE_OPS' && <PipelineHealthStudio />}
            {activeTab === 'WATCHTOWER' && <SentinelWatchtower />}
            {activeTab === 'GOVT_DIRECTIVE' && <GovernmentReportStudio selectedPreset={selectedPresetId} analytics={analytics} />}
            {activeTab === 'HITL_STUDIO' && <HITLStudio />}
          </React.Suspense>
        </ErrorBoundary>
      </div>

      {/* Query History & Session Replay Modal */}
      <QueryHistoryModal
        isOpen={isHistoryOpen}
        onClose={() => setIsHistoryOpen(false)}
        onSelectRun={handleReplayRun}
      />

      {/* Export Artifacts Modal */}
      {isExportOpen && (
        <ExportModal
          analytics={analytics}
          selectedPreset={selectedPresetId}
          onClose={() => setIsExportOpen(false)}
        />
      )}

      {/* Data Licensing Modal */}
      {isLicensingOpen && (
        <DataLicensingModal
          onClose={() => setIsLicensingOpen(false)}
        />
      )}

      {/* Model Benchmarking Disclosure Modal */}
      {isBenchmarkingOpen && (
        <ModelBenchmarkingModal
          onClose={() => setIsBenchmarkingOpen(false)}
        />
      )}

      {/* System Engineering Scope & Roadmap Modal */}
      {isRoadmapOpen && (
        <SystemRoadmapModal
          onClose={() => setIsRoadmapOpen(false)}
        />
      )}

      {/* 4x Optical Chip Magnifier Modal */}
      {inspectedChip && (
        <PixelChipMagnifier
          card={inspectedChip}
          onClose={() => setInspectedChip(null)}
        />
      )}
    </div>
  );
}
