# `server/config.py`

## File Overview

- Purpose: Central configuration for the server.
- Why it exists: Stores constants, paths, and environment variable bindings in one place.
- Architecture fit: Supplies configuration to all other backend modules.

## Detailed Walkthrough

- **Paths**: Dynamically resolves `PROJECT_ROOT`, `SERVER_DIR`, `UPLOADS_DIR`, and `CLIPS_DIR` relative to the current file. Creates data directories if they don't exist.
- **Upload Constraints**: Reads max upload size from env (`CSPOTLIGHT_MAX_UPLOAD_MB`) and defines allowed video extensions.
- **Processing**: Reads concurrency limit (`CSPOTLIGHT_MAX_WORKERS`) and job time-to-live (`CSPOTLIGHT_JOB_TTL`) from env.
- **CORS**: Parses `CSPOTLIGHT_CORS_ORIGINS` to configure allowed frontend URLs.
- **FFmpeg**: Locates the bundled ffmpeg binary or falls back to the system path.

## Backend Concepts

- 12-factor app configuration (reading from environment).
- Path resolution agnostic to current working directory.
- Dynamic directory provisioning on startup.

## Data Flow

1. Module is imported -> resolves paths and reads environment variables.
2. `UPLOADS_DIR` and `CLIPS_DIR` are created immediately if missing.
3. Variables are cached at module level for other imports to use.

## Engineering Decisions

- Creating data directories on import ensures the app doesn't crash later on I/O operations.
- Providing sensible defaults (e.g., 500MB, 2 workers) means it runs out of the box without `.env` files.
- Pathlib is used over `os.path` for robust cross-platform path manipulations.

## Dependencies

- `os`
- `pathlib`

## Interview Questions

- Easy: Why are we creating directories on import?
- Medium: Why use `pathlib.Path` instead of string concatenation?
- Deep: What happens if `import config` is called multiple times in different modules?

## Resume Points

- Implemented a 12-factor compliant configuration module with dynamic path resolution and fallback defaults.

## Improvements

- Use Pydantic `BaseSettings` for stricter type checking and validation of environment variables.

## Checklist

- Ensure all env vars are documented.
- Know how path resolution works.
