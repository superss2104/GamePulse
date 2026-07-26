import logging

from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse

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
