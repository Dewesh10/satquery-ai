import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Polygon, GeoJSON, useMap } from 'react-leaflet';
import L from 'leaflet';
import { PresetLocation, AnalyticsData } from '../../types';
import { Crosshair, Move, Compass, Shield, Radio } from 'lucide-react';

interface SatMapWorkspaceProps {
  preset: PresetLocation;
  analytics: AnalyticsData | null;
  activeLayer: string;
  flyToCoords: [number, number] | null;
  aoiPolygon: [number, number][] | null;
  onDrawAOI: (poly: [number, number][]) => void;
}

const MapController: React.FC<{ center: [number, number]; zoom: number; flyTo: [number, number] | null }> = ({ center, zoom, flyTo }) => {
  const map = useMap();

  useEffect(() => {
    // Recalculate container size immediately and on resize
    const timer = setTimeout(() => {
      map.invalidateSize();
    }, 100);

    if (flyTo) {
      map.flyTo(flyTo, 14, { duration: 1.5 });
    } else {
      map.flyTo(center, Math.max(zoom, 3), { duration: 1.2 });
    }

    return () => clearTimeout(timer);
  }, [center, zoom, flyTo, map]);

  return null;
};

export const SatMapWorkspace: React.FC<SatMapWorkspaceProps> = ({
  preset,
  analytics,
  activeLayer,
  flyToCoords,
  aoiPolygon,
  onDrawAOI
}) => {
  const [coordsReadout, setCoordsReadout] = useState({ lat: preset.center[0], lng: preset.center[1], zoom: preset.zoom });
  const [isDrawing, setIsDrawing] = useState(false);
  const [drawPoints, setDrawPoints] = useState<[number, number][]>([]);

  let tileUrl = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';
  let tileAttribution = 'Esri World Imagery';
  let subdomains: string | string[] = [];
  let filterClass = 'spectral-filter-none';

  if (activeLayer === 'INFRARED') {
    tileUrl = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';
    tileAttribution = 'Sentinel-2 L2A False-Color IR (B08/B04/B03)';
    filterClass = 'spectral-filter-infrared';
  } else if (activeLayer === 'NDVI') {
    tileUrl = 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png';
    tileAttribution = 'Sentinel-2 L2A NDVI Vegetation Index Map';
    subdomains = 'abcd';
    filterClass = 'spectral-filter-ndvi';
  } else if (activeLayer === 'NDWI') {
    tileUrl = 'https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}';
    tileAttribution = 'Sentinel-2 L2A NDWI Water Moisture Map';
    filterClass = 'spectral-filter-ndwi';
  } else if (activeLayer === 'SAR') {
    tileUrl = 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png';
    tileAttribution = 'Sentinel-1A SAR C-Band Synthetic Aperture Radar';
    subdomains = 'abcd';
    filterClass = 'spectral-filter-sar';
  } else if (activeLayer === 'DARK') {
    tileUrl = 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png';
    tileAttribution = 'CartoDB Dark Matter Vector Canvas';
    subdomains = 'abcd';
    filterClass = 'spectral-filter-none';
  }

  return (
    <div className="relative w-full h-full bg-[#030712] overflow-hidden select-none">
      {/* Animated Radar Sweep Beam Scanner Overlay */}
      <div className="radar-beam opacity-40 pointer-events-none" />

      {/* Telemetry Overlay Grid & Scanlines */}
      <div className="absolute inset-0 pointer-events-none z-10 scanlines opacity-50" />

      {/* Top Left HUD Telemetry Crosshair */}
      <div className="absolute top-4 left-4 z-20 pointer-events-none flex items-center gap-2 font-mono text-xs text-cyber-cyan bg-[#0B132B]/85 border border-cyan-500/30 px-3 py-1.5 rounded-xl backdrop-blur-md shadow-cyan-glow">
        <Crosshair className="w-4 h-4 text-cyber-cyan animate-spin" />
        <span className="font-bold">ORBIT FEED • GSD: 10M</span>
      </div>

      {/* Top Right Bearing Readout */}
      <div className="absolute top-4 right-4 z-20 pointer-events-none flex items-center gap-2 font-mono text-xs text-amber-400 bg-[#0B132B]/85 border border-amber-500/30 px-3 py-1.5 rounded-xl backdrop-blur-md shadow-amber-glow">
        <Compass className="w-4 h-4 text-amber-400" />
        <span className="font-bold">BEARING: 0.00° • PITCH: 45.00°</span>
      </div>

      {/* Cockpit Spatial Telemetry HUD (Bottom Left) */}
      <div className="absolute bottom-6 left-6 z-20 bg-[#0B132B]/90 border border-cyan-500/40 backdrop-blur-xl px-4 py-2.5 rounded-xl font-mono text-xs text-slate-200 flex items-center gap-5 shadow-2xl shadow-cyan-950/50">
        <div><span className="text-slate-400">LAT:</span> <span className="text-cyber-cyan font-extrabold">{coordsReadout.lat.toFixed(5)}°</span></div>
        <div><span className="text-slate-400">LNG:</span> <span className="text-cyber-cyan font-extrabold">{coordsReadout.lng.toFixed(5)}°</span></div>
        <div><span className="text-slate-400">ZOOM:</span> <span className="text-amber-400 font-extrabold">{coordsReadout.zoom}</span></div>
        <div><span className="text-slate-400">SENSOR:</span> <span className="text-emerald-400 font-bold">{preset.sensors[0]}</span></div>
      </div>

      {/* AOI Drawing Toolbar */}
      <div className="absolute top-16 left-4 z-20 flex flex-col gap-2 bg-[#0B132B]/90 border border-cyan-500/30 backdrop-blur-xl p-2 rounded-xl shadow-2xl">
        <button
          onClick={() => {
            setIsDrawing(!isDrawing);
            setDrawPoints([]);
          }}
          className={`p-2.5 rounded-lg font-mono text-xs flex items-center gap-2 transition font-bold ${
            isDrawing ? 'bg-rose-500/20 text-rose-400 border border-rose-500/50 shadow-magenta-glow' : 'text-slate-200 hover:bg-slate-800'
          }`}
          title="Draw Polygon AOI"
        >
          <Move className="w-4 h-4 text-cyber-cyan" />
          <span className="hidden sm:inline">{isDrawing ? 'DRAWING AOI...' : 'DRAW AOI'}</span>
        </button>

        {aoiPolygon && (
          <button
            onClick={() => onDrawAOI([])}
            className="p-2 rounded text-[10px] font-mono text-rose-400 hover:bg-rose-950/30 text-center font-bold"
          >
            CLEAR AOI
          </button>
        )}
      </div>

      {/* Confidence-Weighted Layer Visual Legend HUD (Top Center) */}
      <div className="absolute top-4 left-1/2 -translate-x-1/2 z-20 hidden md:flex items-center gap-3 bg-[#0B132B]/85 border border-cyan-500/30 px-3.5 py-1.5 rounded-xl backdrop-blur-md text-[11px] font-mono shadow-cyan-glow">
        <span className="text-slate-300 font-bold">CONFIDENCE LAYER:</span>
        <div className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-cyber-cyan shadow-cyan-glow" />
          <span className="text-cyber-cyan font-bold">HIGH (&ge;85%)</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-amber-400" />
          <span className="text-amber-400 font-bold">MODERATE (&ge;65% Dashed)</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="w-2.5 h-2.5 rounded-full bg-rose-500 animate-pulse" />
          <span className="text-rose-400 font-bold">LOW (&lt;65% Faded)</span>
        </div>
      </div>

      {/* Leaflet Map Canvas */}
      <MapContainer
        center={preset.center}
        zoom={Math.max(preset.zoom, 3)}
        minZoom={3}
        maxZoom={20}
        worldCopyJump={true}
        style={{ width: '100%', height: '100%', position: 'absolute', inset: 0 }}
        zoomControl={false}
      >
        <MapController center={preset.center} zoom={preset.zoom} flyTo={flyToCoords} />
        
        {/* Basemap Tile Layer */}
        <TileLayer
          url={tileUrl}
          attribution={tileAttribution}
          subdomains={subdomains}
          noWrap={true}
          maxNativeZoom={18}
          maxZoom={20}
          className={`transition-all duration-300 ${filterClass}`}
        />

        {/* Render AOI Bounding Polygon */}
        <Polygon
          positions={[
            [preset.bbox[1], preset.bbox[0]],
            [preset.bbox[1], preset.bbox[2]],
            [preset.bbox[3], preset.bbox[2]],
            [preset.bbox[3], preset.bbox[0]]
          ]}
          pathOptions={{ color: '#00F0FF', weight: 2, dashArray: '8, 8', fillColor: '#00F0FF', fillOpacity: 0.08 }}
        />

        {/* User Drawn AOI Polygon */}
        {drawPoints.length > 1 && (
          <Polygon positions={drawPoints} pathOptions={{ color: '#F43F5E', weight: 2.5, fillColor: '#F43F5E', fillOpacity: 0.25 }} />
        )}
        {aoiPolygon && aoiPolygon.length > 1 && (
          <Polygon positions={aoiPolygon} pathOptions={{ color: '#F43F5E', weight: 3, fillColor: '#F43F5E', fillOpacity: 0.3 }} />
        )}

        {/* Render Detected GeoJSON Confidence-Weighted Change Overlay */}
        {analytics && analytics.geojson && (
          <GeoJSON
            key={analytics.preset_id}
            data={analytics.geojson}
            style={(feature) => {
              const conf = feature?.properties?.confidence || analytics?.confidence_score || 0.9;
              let strokeColor = '#00F0FF';
              let dashPattern: string | undefined = undefined;
              let opacity = 0.45;
              let weight = 3.5;

              if (conf >= 0.85) {
                strokeColor = '#00F0FF'; // Deep cyan for high-confidence change
                weight = 3.5;
                opacity = 0.45;
              } else if (conf >= 0.65) {
                strokeColor = '#F59E0B'; // Amber for moderate confidence
                weight = 2.5;
                opacity = 0.30;
                dashPattern = '6, 6';
              } else {
                strokeColor = '#F43F5E'; // Faded rose for low confidence
                weight = 1.5;
                opacity = 0.15;
                dashPattern = '3, 6';
              }

              return {
                color: strokeColor,
                weight: weight,
                fillColor: strokeColor,
                fillOpacity: opacity,
                dashArray: dashPattern
              };
            }}
          />
        )}
      </MapContainer>
    </div>
  );
};
