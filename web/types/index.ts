export type JobStatus = "queued" | "processing" | "completed" | "failed";

export type ClipCategory = "SINGLE_KILL" | "MULTIPLE_KILLS";

export interface ProcessingSettings {
  disable_single_kills: boolean;
  disable_multi_kills: boolean;
  motion_weight: number | null;
  audio_weight: number | null;
  killfeed_weight: number | null;
}

export interface ProcessRequest {
  job_id: string;
  settings: ProcessingSettings;
}

export interface UploadResponse {
  job_id: string;
  filename: string;
  size_bytes: number;
}

export interface ProcessResponse {
  job_id: string;
  status: JobStatus;
}

export interface ClipResult {
  name: string;
  start: number;
  end: number;
  duration: number;
  category: ClipCategory;
  download_url: string;
}

export interface ProcessingResult {
  clip_count: number;
  clips: ClipResult[];
}

export interface JobStatusResponse {
  job_id: string;
  status: JobStatus;
  progress?: string;
  error?: string;
  result?: ProcessingResult;
  created_at?: string;
}

export interface ErrorResponse {
  detail: string;
}

export interface UploadState {
  file: File | null;
  uploading: boolean;
  uploadProgress: number;
  error: string | null;
}

export const DEFAULT_SETTINGS: ProcessingSettings = {
  disable_single_kills: false,
  disable_multi_kills: false,
  motion_weight: null,
  audio_weight: null,
  killfeed_weight: null,
};
