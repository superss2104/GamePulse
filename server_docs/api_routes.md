    # `server/api/routes.py`

## File Overview

- Purpose: Defines HTTP API endpoints.
- Why it exists: Exposes functionality (upload, process, status, download) to the client.
- Architecture fit: The controller layer that validates requests and delegates to services.

## Detailed Walkthrough

- `POST /upload`: Validates extension, generates `job_id`, streams file to disk in chunks, and registers the job.
- `POST /process`: Takes `job_id` and settings, and submits the job to the `job_manager` for background processing.
- `GET /results/{job_id}`: Polls the `job_manager` to return the current status, progress, or completed results.
- `GET /download/{job_id}/{filename}`: Verifies job completion and serves the generated MP4 clip using `FileResponse`.

## Backend Concepts

- Streaming large file uploads to disk to avoid memory bloat.
- Asynchronous route handlers (`async def`).
- Decoupling upload from processing (job queue pattern).

## Data Flow

1. Upload -> File written in chunks -> Job registered -> returns `job_id`.
2. Process -> `job_manager.submit` called -> returns 202 Accepted.
3. Polling -> `job_manager.get_job` checked -> returns status/metadata.
4. Download -> `FileResponse` serves file from disk.

## Engineering Decisions

- Processing is detached from the upload request to prevent HTTP timeouts for long-running video tasks.
- Uploads are chunk-streamed to handle potentially gigabyte-sized game recordings safely.
- Statuses return clear HTTP errors (404, 409, 413) based on domain logic.

## Dependencies

- `fastapi`
- `logging`
- `models.schemas`
- `processing.worker`
- `services.storage`

## Interview Questions

- Easy: Why is the upload streamed in chunks?
- Medium: Why does `/process` return a 202 status code instead of waiting for the result?
- Deep: How does `FileResponse` handle serving large files efficiently?

## Resume Points

- Designed an asynchronous API handling gigabyte-scale streaming file uploads and asynchronous background processing.

## Improvements

- Rate limit `/upload` to prevent storage exhaustion.
- Authenticate requests or tie jobs to user sessions.

## Checklist

- Understand the error codes returned.
- Know why upload and process are separate endpoints.
