import logging
import shutil
import uuid
from pathlib import Path

from server.config import ALLOWED_EXTENSIONS, CLIPS_DIR, UPLOADS_DIR

LOGGER = logging.getLogger(__name__)


def generate_job_id() -> str:
    return uuid.uuid4().hex[:12]

def validate_extension(filename: str) -> bool:
    ext = Path(filename).suffix.lower()
    return ext in ALLOWED_EXTENSIONS


def get_upload_path(job_id: str, filename: str) -> Path:
    job_dir = UPLOADS_DIR / job_id
    job_dir.mkdir(parents=True, exist_ok=True)
    return job_dir / filename


def get_clips_dir(job_id: str) -> Path:
    job_clips = CLIPS_DIR / job_id
    job_clips.mkdir(parents=True, exist_ok=True)
    return job_clips


def get_clip_path(job_id: str, clip_name: str) -> Path | None:
    path = CLIPS_DIR / job_id / clip_name
    return path if path.exists() else None


def list_clips(job_id: str) -> list[Path]:
    job_clips = CLIPS_DIR / job_id
    if not job_clips.exists():
        return []
    return sorted(job_clips.glob("clip_*.mp4"))

def cleanup_job(job_id: str) -> None:
    for base_dir in (UPLOADS_DIR, CLIPS_DIR):
        job_dir = base_dir / job_id
        if job_dir.exists():
            shutil.rmtree(job_dir, ignore_errors=True)
            LOGGER.info("Cleaned up %s", job_dir)
