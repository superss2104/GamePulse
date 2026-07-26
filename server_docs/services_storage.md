# `server/services/storage.py`

## File Overview

- Purpose: Manages file I/O and paths on disk.
- Why it exists: Centralizes all logic for creating, finding, and deleting video files.
- Architecture fit: The storage layer.

## Detailed Walkthrough

- `generate_job_id()`: Creates a unique 12-character hex ID.
- `validate_extension()`: Checks if an upload matches allowed video formats.
- `get_upload_path()`: Returns path for the raw upload, creating the directory.
- `get_clips_dir()` / `get_clip_path()`: Manages paths for the generated highlight chunks.
- `cleanup_job()`: Recursively deletes a job's upload and clips directories using `shutil.rmtree`.

## Backend Concepts

- File system manipulation.
- UUID generation for collision-free namespacing.
- Defensive I/O (handling missing files/folders gracefully).

## Data Flow

1. Upload -> `get_upload_path` -> File written to disk.
2. Processing -> `get_clips_dir` -> FFmpeg writes clips here.
3. Download -> `get_clip_path` -> Verifies file exists before serving.
4. Expiry -> `cleanup_job` -> Wipes disk footprint.

## Engineering Decisions

- Grouping files by `job_id` folders (e.g., `uploads/<job_id>/video.mp4` and `clips/<job_id>/clip_1.mp4`) makes cleanup completely trivial (just delete the folder) without risking orphaned files.
- Utilizing `pathlib` for all operations ensures cross-platform compatibility (Windows vs Linux).

## Dependencies

- `uuid`
- `pathlib`
- `shutil`
- `server.config`

## Interview Questions

- Easy: Why group files by `job_id` instead of putting them all in one folder?
- Medium: What does `shutil.rmtree(..., ignore_errors=True)` do, and why is it useful here?
- Deep: How would you modify this file to upload to AWS S3 instead of local disk?

## Resume Points

- Implemented structured local file management with robust lifecycle cleanup for large media assets.

## Improvements

- Add a migration path to abstract storage behind an interface (e.g., LocalStorage vs S3Storage).

## Checklist

- Ensure paths use `Path` objects consistently.
