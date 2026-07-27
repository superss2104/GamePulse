import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PIPELINE_SRC_DIR = PROJECT_ROOT / "src"

# Server data directories
SERVER_DIR = Path(__file__).resolve().parent
UPLOADS_DIR = SERVER_DIR / "uploads"
CLIPS_DIR = SERVER_DIR / "clips"

# Ensure data directories exist at import time.
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
CLIPS_DIR.mkdir(parents=True, exist_ok=True)


MAX_UPLOAD_SIZE_MB = int(os.getenv("CSPOTLIGHT_MAX_UPLOAD_MB", "2000"))
MAX_UPLOAD_SIZE_BYTES = MAX_UPLOAD_SIZE_MB * 1024 * 1024

ALLOWED_EXTENSIONS = {".mp4", ".avi", ".mkv", ".mov", ".webm"}

# Maximum number of concurrent processing jobs.
MAX_WORKERS = int(os.getenv("CSPOTLIGHT_MAX_WORKERS", "2"))

# Auto-delete job data after this many seconds (default: 1 hour).
JOB_TTL_SECONDS = int(os.getenv("CSPOTLIGHT_JOB_TTL", "3600"))

CORS_ORIGINS = os.getenv(
    "CSPOTLIGHT_CORS_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000",
).split(",")

LOCAL_FFMPEG = PROJECT_ROOT / "ffmpeg" / "bin" / "ffmpeg.exe"
FFMPEG_PATH = str(LOCAL_FFMPEG) if LOCAL_FFMPEG.exists() else "ffmpeg"
