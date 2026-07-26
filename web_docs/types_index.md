# `web/types/index.ts`

## File Overview

- Purpose: Shared type definitions and default settings.
- Why it exists: It keeps frontend state and backend API contracts aligned.
- Architecture fit: It is the schema layer for the UI.

## Detailed Walkthrough

- `JobStatus` defines the job lifecycle.
- `ClipCategory` defines clip classification values.
- `ProcessingSettings` defines the `/process` request body settings.
- `ProcessRequest` is the full processing request type.
- `UploadResponse` contains the `job_id` returned after upload.
- `ProcessResponse` confirms processing started.
- `ClipResult` describes one generated clip.
- `ProcessingResult` groups the clip list and count.
- `JobStatusResponse` drives the polling UI.
- `ErrorResponse` is the generic backend error shape.
- `UploadState` is a UI-only helper type.
- `DEFAULT_SETTINGS` provides the initial toggle state.

## React / Frontend Concepts

- Prop typing
- State typing
- API response typing

## Engineering Decisions

- Matching backend-shaped contracts reduces drift between layers.
- Keeping `DEFAULT_SETTINGS` in types gives the app one source of truth for defaults.

## Dependencies

- TypeScript

## Interview Questions

- Easy: What is `JobStatus`?
- Medium: Why keep backend-like types in the frontend?
- Deep: What breaks if the backend changes a field name?
- Design: Would you share these types in a monorepo?
- Follow-up: Why are some fields optional in `JobStatusResponse`?

## Resume Points

- Defined end-to-end TypeScript contracts for upload, processing, and clip results.

## Improvements

- Split into request, response, and UI type files if the project grows.

## Checklist

- Know request vs response vs UI types.
- Know which file imports `DEFAULT_SETTINGS`.

