# `web/lib/api.ts`

## File Overview

- Purpose: Central API client.
- Why it exists: It isolates all backend communication in one typed module.
- Architecture fit: It is the bridge between UI state and backend jobs.

## Detailed Walkthrough

- `API_BASE` reads `NEXT_PUBLIC_API_URL` or falls back to `http://localhost:8000`.
- `ApiError` stores a message and HTTP status.
- `handleResponse<T>()` parses successful JSON and converts failures into `ApiError`.
- `uploadVideo(file, onProgress)` uploads the file with `XMLHttpRequest` so progress events are available.
- `startProcessing(jobId, settings)` sends the processing request to `/process`.
- `getJobStatus(jobId)` fetches `/results/:jobId`.
- `getDownloadUrl(jobId, clipName)` builds a clip download URL.
- `pollUntilDone(jobId, onUpdate, intervalMs)` keeps polling until the backend reports `completed` or `failed`.

## React / Frontend Concepts

- Not a component file, but it supports component state and effects.
- Async request orchestration.
- Error normalization.

## Data Flow

1. Upload file -> backend returns `job_id`.
2. Send `job_id + settings` -> backend starts processing.
3. Poll `/results/:jobId` until terminal state.
4. Build download URLs for clips.

## Engineering Decisions

- XHR is used for upload progress because fetch does not provide upload progress callbacks.
- Polling is used because processing is asynchronous and the backend is job-based.
- The module stays small and explicit so components do not duplicate request logic.

## Dependencies

- Browser `fetch`
- `XMLHttpRequest`
- `FormData`
- TypeScript

## Interview Questions

- Easy: Why not use fetch for upload progress?
- Medium: Why is polling implemented in a loop?
- Deep: What are the tradeoffs of polling versus SSE or websockets?
- Design: How would you add retries or cancellation?
- Follow-up: What should happen if the backend returns invalid JSON?

## Resume Points

- Centralized backend integration into a typed API layer.
- Added upload progress tracking and job polling for async processing.

## Improvements

- Add abort/cancel handling.
- Add retry/backoff.
- Validate response shapes more strictly.

## Checklist

- Know the endpoint contract.
- Know why XHR is used.
- Know how polling terminates.

