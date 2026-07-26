from __future__ import annotations

from datetime import datetime
from enum import Enum


from pydantic import BaseModel, Field

class JobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"



class ProcessingSettings(BaseModel):
    motion_weight: float | None = None
    audio_weight: float | None = None
    killfeed_weight: float | None = None

class ProcessRequest(BaseModel):
    job_id: str
    settings: ProcessingSettings = Field(default_factory=ProcessingSettings)

class UploadResponse(BaseModel):
    job_id: str
    filename: str
    size_bytes: int

class ProcessResponse(BaseModel):
    job_id: str
    status: JobStatus

class ClipResult(BaseModel):
    name: str
    start: float
    end: float
    duration: float
    download_url: str

class ProcessingResult(BaseModel):
    clip_count: int
    clips: list[ClipResult]


class JobStatusResponse(BaseModel):
    job_id: str
    status: JobStatus
    progress: str | None = None
    error: str | None = None
    result: ProcessingResult | None = None
    created_at: datetime | None = None


class ErrorResponse(BaseModel):
    detail: str
