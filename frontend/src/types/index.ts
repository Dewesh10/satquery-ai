export interface PresetLocation {
  name: string;
  category: string;
  center: [number, number];
  zoom: number;
  bbox: [number, number, number, number];
  dates: [string, string];
  sensors: string[];
  suggested_prompt: string;
}

export interface STACScene {
  id: string;
  collection: string;
  preset_id: string;
  title: string;
  datetime: string;
  sensor: string;
  modality: 'OPTICAL' | 'SAR';
  cloud_cover: number;
  gsd_meters: number;
  bbox: [number, number, number, number];
  center: [number, number];
  bands: string[];
  sun_elevation: number;
  thumbnail: string;
  stac_url: string;
}

export interface DAGStep {
  step_id: number;
  name: string;
  tool: string;
  status: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED' | 'FAILED';
  output: Record<string, any>;
}

export interface QueryPlan {
  query: string;
  selected_preset_id: string;
  preset: PresetLocation;
  intent: string;
  dag_steps: DAGStep[];
  execution_time_ms: number;
}

export interface EvidenceCard {
  id: string;
  title: string;
  scene_id: string;
  sensor: string;
  timestamp: string;
  coordinates: [number, number];
  metric: string;
  confidence: string;
  thumbnail: string;
  type: string;
}

export interface EvidenceData {
  answer: string;
  provenance: {
    scenes_referenced: string[];
    sensors: string[];
    timestamps: string[];
    modality: string;
    verification_status: string;
  };
  evidence_cards: EvidenceCard[];
}

export interface TimeSeriesPoint {
  year?: string;
  date?: string;
  time?: string;
  built_up_sq_km?: number;
  forest_sq_km?: number;
  water_sq_km?: number;
  vessels?: number;
  reclaimed_sq_km?: number;
  density_pct?: number;
  ndvi_mean?: number;
}

export interface UncertaintyMetrics {
  calibrated_trust_score?: number;
  error_margin_pct?: string;
  cloud_interference_pct?: string;
  temporal_gap?: string;
  co_registration_rmse_px?: string;
  uncertainty_status?: string;
}

export interface OpsMetrics {
  compute_cost_usd?: number;
  cache_hit_rate?: string;
  gpu_vram_mb?: number;
  national_scale_cost_est_usd?: string;
  bhuvan_nrsc_compliance?: string;
}

export interface GroundTruthValidation {
  official_agency: string;
  official_metric_name: string;
  satquery_value: string;
  official_value: string;
  alignment_percentage: string;
  verification_doc: string;
}

export interface AnalyticsData {
  preset_id: string;
  primary_metric_label: string;
  primary_metric_value: string;
  percentage_change: string;
  pixel_delta_count: number;
  confidence_score: number;
  area_sq_km: number;
  hectares: number;
  structural_count: number;
  time_span: string;
  geojson: any;
  time_series: TimeSeriesPoint[];
  uncertainty?: UncertaintyMetrics;
  ops_metrics?: OpsMetrics;
  ground_truth_validation?: GroundTruthValidation | null;
}

export interface QueryResponse {
  run_id: string;
  plan: QueryPlan;
  analytics: AnalyticsData;
  evidence: EvidenceData;
  timeline: any[];
}
