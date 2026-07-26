# `server/processing/worker.py`

## File Overview

- Purpose: Background job manager and executor.
- Why it exists: Runs CPU-intensive video processing in a separate thread so it doesn't block the API event loop.
- Architecture fit: The async task runner of the backend.

## Detailed Walkthrough

- `Job`: Data class holding the state, progress, and result of a single processing task.
- `JobManager`: Thread-safe singleton managing a dictionary of jobs.
- `submit()`: Validates job state and submits `_run_job` to the `ThreadPoolExecutor`.
- `_run_job()`: The worker thread logic. Updates status, calls `process_video()`, handles exceptions, and saves results.
- `cleanup_expired()`: Scans for jobs older than `JOB_TTL_SECONDS` and deletes their data.

## Backend Concepts

- Thread-safe state management (`threading.Lock`).
- Background task execution (`ThreadPoolExecutor`).
- In-memory job queuing.

## Data Flow

1. Route calls `register()` -> Job created in `_jobs` dict.
2. Route calls `submit()` -> Job pushed to ThreadPool.
3. Worker thread takes job -> sets `PROCESSING` -> runs heavy pipeline -> sets `COMPLETED`/`FAILED`.
4. Route polls `get_job()` -> reads latest state.

## Engineering Decisions

- Using `ThreadPoolExecutor` instead of `ProcessPoolExecutor` because FastAPI is async, and OpenCV/FFmpeg release the GIL, so threads work well without multiprocessing overhead.
- A thread lock (`_lock`) is used strictly around dictionary mutations to prevent race conditions.
- Uses an in-memory queue instead of Redis/Celery for simplicity and ease of deployment for a portfolio project.

## Dependencies

- `threading`
- `concurrent.futures`
- `services.pipeline`
- `services.storage`

## Interview Questions

- Easy: Why is a `threading.Lock` used when updating the job dictionary?
- Medium: Why use a thread pool instead of `asyncio.create_task`?
- Deep: What are the risks of an in-memory job queue if the server restarts? How would you fix it?

## Resume Points

- Built a thread-safe background job manager to decouple heavy computer vision tasks from the HTTP API.

## Improvements

- Migrate to Celery and Redis/RabbitMQ for persistence and distributed scaling.
- Implement job cancellation.

## Checklist

- Understand why a lock is necessary.
- Know the limitations of this in-memory approach.
