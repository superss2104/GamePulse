import logging
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel

from server.config import MAX_UPLOAD_SIZE_BYTES
from server.models.schemas import (
    ErrorResponse,
    JobStatus,
    JobStatusResponse,
    ProcessRequest,
    ProcessResponse,
    UploadResponse,
)
from server.processing.worker import job_manager
from server.services.storage import (
    generate_job_id,
    get_clip_path,
    get_upload_path,
    validate_extension,
)

LOGGER = logging.getLogger(__name__)

# Pre-loaded demo clips that users can process without uploading.
DEMO_VIDEOS_DIR = Path(__file__).resolve().parent.parent / "demo_videos"

DEMO_CLIPS = {
    "test13": {
        "filename": "test13.mp4",
        "title": "AWP Flick Shot",
    },
    "test6": {
        "filename": "test6.mp4",
        "title": "3 kills highlight",
    },
}

router = APIRouter()

@router.post( #Bind function below to handle POST requests at the /upload endpoint
    "/upload",
    response_model=UploadResponse,
    status_code=201,
    responses={400: {"model": ErrorResponse}, 413: {"model": ErrorResponse}},
    summary="Upload a video file"
)
async def upload_video(file: UploadFile = File(...)): #... indicates file is a required parameter
    if not file.filename or not validate_extension(file.filename):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Allowed: .mp4, .avi, .mkv, .mov, .webm"
        )

    job_id = generate_job_id()
    save_path = get_upload_path(job_id, file.filename)

    size = 0
    with open(save_path, "wb") as f:
        while chunk := await file.read(1024 * 1024):  # process 1mb chunks so that video files don't crash the server.
            size += len(chunk)
            if size > MAX_UPLOAD_SIZE_BYTES: # Clean up the partial file and send HTTP 413 error.
                f.close()
                save_path.unlink(missing_ok=True)
                raise HTTPException(
                    status_code=413,
                    detail=f"File too large. Maximum size: {MAX_UPLOAD_SIZE_BYTES // (1024*1024)} MB"
                )
            f.write(chunk)

    job_manager.register(job_id, str(save_path))

    LOGGER.info("Upload complete: job=%s file=%s size=%d bytes", job_id, file.filename, size)
    return UploadResponse(job_id=job_id, filename=file.filename, size_bytes=size)


@router.post(
    "/process",
    response_model=ProcessResponse,
    status_code=202,
    responses={404: {"model": ErrorResponse}, 409: {"model": ErrorResponse}},
    summary="Start processing an uploaded video",
)
async def process_video(request: ProcessRequest):
    try:
        job = job_manager.submit(request.job_id, request.settings)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Job {request.job_id} not found")
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    return ProcessResponse(job_id=job.id, status=job.status)

@router.get(
    "/results/{job_id}",
    response_model=JobStatusResponse,
    responses={404: {"model": ErrorResponse}},
    summary="Get processing status and results",
)
async def get_results(job_id: str):
    job = job_manager.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")

    return JobStatusResponse(
        job_id=job.id,
        status=job.status,
        progress=job.progress,
        error=job.error,
        result=job.result,
        created_at=job.created_at,
    )

@router.get(
    "/download/{job_id}/{filename}",
    responses={404: {"model": ErrorResponse}},
    summary="Download a generated clip",
)
async def download_clip(job_id: str, filename: str):
    job = job_manager.get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    if job.status != JobStatus.COMPLETED:
        raise HTTPException(status_code=409, detail="Job not yet completed")

    clip_path = get_clip_path(job_id, filename)
    if clip_path is None:
        raise HTTPException(status_code=404, detail=f"Clip {filename} not found")

    return FileResponse(
        path=str(clip_path),
        media_type="video/mp4",
        filename=filename,
        headers={"Accept-Ranges": "bytes"},
    )


# --- Demo endpoint: process a pre-loaded sample clip ---

class DemoRequest(BaseModel):
    clip_id: str

class DemoResponse(BaseModel):
    job_id: str
    clip_title: str

@router.post(
    "/demo/process",
    response_model=DemoResponse,
    status_code=202,
    responses={404: {"model": ErrorResponse}},
    summary="Process a pre-loaded demo clip through the pipeline",
)
async def process_demo_clip(request: DemoRequest):
    clip = DEMO_CLIPS.get(request.clip_id)
    if clip is None:
        raise HTTPException(
            status_code=404,
            detail=f"Demo clip '{request.clip_id}' not found. Available: {list(DEMO_CLIPS.keys())}",
        )

    video_path = DEMO_VIDEOS_DIR / clip["filename"]
    if not video_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Demo video file not found on server: {clip['filename']}",
        )

    # Register and immediately submit for processing (skip the upload step).
    job_id = generate_job_id()
    job_manager.register(job_id, str(video_path))
    job_manager.submit(job_id)

    LOGGER.info("Demo processing started: job=%s clip=%s", job_id, request.clip_id)
    return DemoResponse(job_id=job_id, clip_title=clip["title"])

