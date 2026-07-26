import logging
import sys


from server.config import PIPELINE_SRC_DIR
from server.models.schemas import (
    ClipResult,
    ProcessingResult,
    ProcessingSettings,
)
from server.services.storage import get_clips_dir

LOGGER = logging.getLogger(__name__)

_src_path = str(PIPELINE_SRC_DIR)
if _src_path not in sys.path:
    sys.path.insert(0, _src_path) #Insert it in the beginning since python searches from left to right. This is to prevent incorrect imports.


def process_video(
    video_path: str,
    job_id: str,
    settings: ProcessingSettings | None = None
) -> ProcessingResult:

    if settings is None:
        settings = ProcessingSettings()


    from highlight.pipeline import detect_highlights
    from video.clips import cut_clips

    LOGGER.info("Starting pipeline for job %s: %s", job_id, video_path)
    clips = detect_highlights(
        video_path,
        motion_weight=settings.motion_weight,
        audio_weight=settings.audio_weight,
        killfeed_weight=settings.killfeed_weight,
    )
    LOGGER.info("Pipeline detected %d clip(s) for job %s", len(clips), job_id)

    if not clips:
        return ProcessingResult(clip_count=0, clips=[])
    output_dir = get_clips_dir(job_id)
    cut_clips(video_path, clips, output_dir=str(output_dir))

    clip_results: list[ClipResult] = []
    for i, (start, end) in enumerate(clips):
        clip_name = f"clip_{i + 1}.mp4"
        clip_results.append(ClipResult(
            name=clip_name,
            start=round(start, 2),
            end=round(end, 2),
            duration=round(end - start, 2),
            download_url=f"/download/{job_id}/{clip_name}",
        ))

    result = ProcessingResult(clip_count=len(clip_results), clips=clip_results)
    LOGGER.info("Job %s complete: %d clips generated", job_id, result.clip_count)
    return result
