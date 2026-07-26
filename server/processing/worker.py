import logging
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone


from server.config import JOB_TTL_SECONDS, MAX_WORKERS
from server.models.schemas import (
    JobStatus,
    ProcessingResult,
    ProcessingSettings,
)
from server.services.pipeline import process_video
from server.services.storage import cleanup_job

LOGGER = logging.getLogger(__name__)


class Job:
    __slots__ = (
        "id", "status", "progress", "video_path", "settings",
        "result", "error", "created_at",
    )

    def __init__(
        self,
        job_id: str,
        video_path: str,
        settings: ProcessingSettings | None = None,
    ):
        self.id: str = job_id
        self.status: JobStatus = JobStatus.QUEUED
        self.progress: str = "Waiting in queue..."
        self.video_path: str = video_path
        self.settings: ProcessingSettings = settings or ProcessingSettings()
        self.result: ProcessingResult | None = None
        self.error: str | None = None
        self.created_at: datetime = datetime.now(timezone.utc)


class JobManager:
    def __init__(self, max_workers: int = MAX_WORKERS):
        self._jobs: dict[str, Job] = {}
        self._lock = threading.Lock()
        self._executor = ThreadPoolExecutor(max_workers=max_workers)

    def register(self, job_id: str, video_path: str) -> Job:
        job = Job(job_id=job_id, video_path=video_path)
        with self._lock:
            self._jobs[job_id] = job
        LOGGER.info("Registered job %s for %s", job_id, video_path)
        return job

    def submit(self, job_id: str, settings: ProcessingSettings | None = None) -> Job:
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                raise KeyError(f"Job {job_id} not found")
            if job.status != JobStatus.QUEUED:
                raise ValueError(f"Job {job_id} is already {job.status.value}")
            job.settings = settings or ProcessingSettings()

        self._executor.submit(self._run_job, job_id)
        LOGGER.info("Submitted job %s for processing", job_id)
        return job

    def get_job(self, job_id: str) -> Job | None:
        with self._lock:
            return self._jobs.get(job_id)

    def cleanup_expired(self) -> int:
        now = datetime.now(timezone.utc)
        expired_ids: list[str] = []

        with self._lock:
            for job_id, job in self._jobs.items():
                age = (now - job.created_at).total_seconds()
                if age > JOB_TTL_SECONDS and job.status in (
                    JobStatus.COMPLETED, JobStatus.FAILED,
                ):
                    expired_ids.append(job_id)

        for job_id in expired_ids:
            cleanup_job(job_id)
            with self._lock:
                self._jobs.pop(job_id, None)
            LOGGER.info("Expired job %s cleaned up", job_id)

        return len(expired_ids)

    def shutdown(self) -> None:
        self._executor.shutdown(wait=False)
        LOGGER.info("Job manager shut down")

    def _run_job(self, job_id: str) -> None:
        with self._lock:
            job = self._jobs.get(job_id)
            if job is None:
                return
            job.status = JobStatus.PROCESSING
            job.progress = "Analyzing video..."

        try:
            result = process_video(
                video_path=job.video_path,
                job_id=job_id,
                settings=job.settings,
            )
            with self._lock:
                job.result = result
                job.status = JobStatus.COMPLETED
                job.progress = "Done"
            LOGGER.info("Job %s completed: %d clips", job_id, result.clip_count)

        except Exception as exc:
            LOGGER.exception("Job %s failed", job_id)
            with self._lock:
                job.status = JobStatus.FAILED
                job.error = str(exc)
                job.progress = "Failed"

job_manager = JobManager()
