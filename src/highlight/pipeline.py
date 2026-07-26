import logging

try:
    from ..audio.analysis import extract_audio_scores
    from ..cs2.deathscreen import extract_death_mask
    from ..cs2.killfeed import extract_killfeed_data
    from ..video.motion import extract_motion_scores
    from .scoring import combine_multiple_scores, normalize_scores
    from .timestamps import (
        DEFAULT_CLIP_LEN_SECONDS,
        DEFAULT_MIN_CLIP_GAP_SECONDS,
        DEFAULT_START_BIAS_SECONDS,
        frames_to_timestamps,
        merge_overlapping_clips,
    )
    from .windows import filter_short_events, merge_windows, percentile_threshold, sliding_windows
except ImportError:  # Support running src/main.py directly.
    from audio.analysis import extract_audio_scores
    from cs2.deathscreen import extract_death_mask
    from cs2.killfeed import extract_killfeed_data
    from highlight.scoring import combine_multiple_scores, normalize_scores
    from highlight.timestamps import (
        DEFAULT_CLIP_LEN_SECONDS,
        DEFAULT_MIN_CLIP_GAP_SECONDS,
        DEFAULT_START_BIAS_SECONDS,
        frames_to_timestamps,
        merge_overlapping_clips,
    )
    from highlight.windows import filter_short_events, merge_windows, percentile_threshold, sliding_windows
    from video.motion import extract_motion_scores

DEFAULT_START_BIAS_SECONDS = -2.0
DEFAULT_CLIP_LEN_SECONDS = 4
DEATH_BACKTRACK_SECONDS = 1.5
DEATH_POST_TRACK_SECONDS = 0.5
MIN_DEATH_DURATION_SECONDS = 0.5
DEATH_MAX_GAP_SECONDS = 0.3

LOGGER = logging.getLogger(__name__)
WINDOW_STEP_FRAMES = 5
WINDOW_PERCENTILE = 50
MIN_EVENT_DURATION_SECONDS = 0.1
MERGE_GAP_SECONDS = 3.5
MOTION_SCORE_WEIGHT = 0.25
AUDIO_SCORE_WEIGHT = 0.25
KILLFEED_SCORE_WEIGHT = 0.5


def detect_highlights(video_path, motion_weight=None, audio_weight=None,
                      killfeed_weight=None):
    motion_scores, fps = extract_motion_scores(video_path)
    scores, kill_counts, death_mask = build_highlight_scores(
        video_path, motion_scores, fps,
        motion_weight, audio_weight, killfeed_weight,
    )

    window_size = max(1, round(fps))
    windows = sliding_windows(scores, window_size, WINDOW_STEP_FRAMES)
    highlight_windows = percentile_threshold(windows, percentile=WINDOW_PERCENTILE)
    merge_gap_frames = max(1, round(fps * MERGE_GAP_SECONDS))
    merged = merge_windows(highlight_windows, max_gap=merge_gap_frames)
    filtered = filter_short_events(merged, fps, MIN_EVENT_DURATION_SECONDS)

    LOGGER.debug("FPS: %.2f, window_size: %d, merge_gap_frames: %d", fps, window_size, merge_gap_frames)
    LOGGER.debug("Merged events (frame ranges): %s", filtered)
    for i, (sf, ef) in enumerate(filtered):
        LOGGER.debug(
            "  Event %d: frames %d-%d  =>  %.2fs - %.2fs  (duration %.2fs)",
            i + 1, sf, ef, sf / fps, ef / fps, (ef - sf) / fps,
        )

    # Trim events so they do not extend past a death screen.
    trimmed = _trim_events_at_death(filtered, death_mask)
    LOGGER.debug("Death-trimmed events: %s", trimmed)

    # Expand events backward using raw motion scores so clips start
    # where the action begins, not where the kill-feed appears.
    # Death frames are excluded from expansion to prevent the pipeline
    # from pulling in the death animation as "action".
    expanded = _expand_events_with_motion(trimmed, motion_scores, fps, death_mask=death_mask)
    LOGGER.debug("Expanded events: %s", expanded)
    for i, (sf, ef) in enumerate(expanded):
        LOGGER.debug(
            "  Expanded %d: frames %d-%d  =>  %.2fs - %.2fs  (duration %.2fs)",
            i + 1, sf, ef, sf / fps, ef / fps, (ef - sf) / fps,
        )

    timestamps = frames_to_timestamps(
        expanded,
        fps,
        clip_len=DEFAULT_CLIP_LEN_SECONDS,
        start_bias=DEFAULT_START_BIAS_SECONDS,
        death_mask=death_mask,
    )
    LOGGER.debug("Pre-merge timestamps: %s", timestamps)
    for i, (s, e) in enumerate(timestamps):
        LOGGER.debug("  Pre-merge clip %d: %.2fs - %.2fs  (duration %.2fs)", i + 1, s, e, e - s)

    final = merge_overlapping_clips(
        timestamps,
        min_gap=DEFAULT_MIN_CLIP_GAP_SECONDS,
    )
    LOGGER.debug("Final timestamps: %s", final)
    for i, (s, e) in enumerate(final):
        LOGGER.debug("  Final clip %d: %.2fs - %.2fs  (duration %.2fs)", i + 1, s, e, e - s)

    return final


def build_highlight_scores(
    video_path, motion_scores, fps,
    motion_weight=None, audio_weight=None, killfeed_weight=None,
):
    if motion_weight is None:
        motion_weight = MOTION_SCORE_WEIGHT
    if audio_weight is None:
        audio_weight = AUDIO_SCORE_WEIGHT
    if killfeed_weight is None:
        killfeed_weight = KILLFEED_SCORE_WEIGHT

    audio_scores = _extract_audio_safe(video_path, fps, len(motion_scores))
    killfeed_scores, kill_counts = _extract_killfeed_safe(video_path, len(motion_scores))
    raw_death_mask = _extract_death_mask_safe(video_path, len(motion_scores))

    # Shift death mask backward to cover the red flash/blood screen 
    # and discard false positive killfeed entries caused by the player's own death.
    death_mask = [False] * len(raw_death_mask)
    if any(raw_death_mask):
        max_gap_frames = int(DEATH_MAX_GAP_SECONDS * fps)
        bridged_raw = list(raw_death_mask)
        last_true = -1
        for i, val in enumerate(bridged_raw):
            if val:
                if last_true != -1 and i - last_true <= max_gap_frames:
                    for j in range(last_true + 1, i):
                        bridged_raw[j] = True
                last_true = i

        # Filter out short false-positive death screens
        min_death_frames = int(MIN_DEATH_DURATION_SECONDS * fps)
        filtered_raw = [False] * len(bridged_raw)
        count = 0
        for i, is_death in enumerate(bridged_raw):
            if is_death:
                count += 1
            else:
                if count >= min_death_frames:
                    for j in range(i - count, i):
                        filtered_raw[j] = True
                count = 0
        if count >= min_death_frames:
            for j in range(len(bridged_raw) - count, len(bridged_raw)):
                filtered_raw[j] = True

        backtrack_frames = int(DEATH_BACKTRACK_SECONDS * fps)
        post_frames = int(DEATH_POST_TRACK_SECONDS * fps)
        for i, is_death in enumerate(filtered_raw):
            if is_death:
                start_idx = max(0, i - backtrack_frames)
                end_idx = min(len(raw_death_mask) - 1, i + post_frames)
                for j in range(start_idx, end_idx + 1):
                    death_mask[j] = True

    if killfeed_scores and any(death_mask):
        suppressed = 0
        for i in range(min(len(killfeed_scores), len(death_mask))):
            if death_mask[i] and killfeed_scores[i] > 0:
                killfeed_scores[i] = 0.0
                if i < len(kill_counts):
                    kill_counts[i] = 0
                suppressed += 1
        LOGGER.info(
            "Death-mask suppression: zeroed %d killfeed scores during death-screen frames",
            suppressed,
        )

    signals = [motion_scores]
    weights = [motion_weight]
    signal_names = ["motion"]

    if audio_scores:
        signals.append(audio_scores)
        weights.append(audio_weight)
        signal_names.append("audio")

    if killfeed_scores:
        signals.append(killfeed_scores)
        weights.append(killfeed_weight)
        signal_names.append("killfeed")

    if len(signals) == 1:
        LOGGER.info("Using motion-only highlight scores")
        return motion_scores, kill_counts, death_mask

    LOGGER.info(
        "Combining %s scores with weights %s",
        " + ".join(signal_names),
        " / ".join(f"{w:.2f}" for w in weights),
    )

    combined_scores = combine_multiple_scores(signals, weights)
  
    if killfeed_scores:
        norm_kf = normalize_scores(killfeed_scores)
        gated = 0
        for i in range(len(combined_scores)):
            kf_val = norm_kf[i] if i < len(norm_kf) else 0.0
            if kf_val == 0.0:
                combined_scores[i] = 0.0
                gated += 1
        LOGGER.info(
            "Killfeed gate: zeroed %d / %d frames without kill-feed activity",
            gated, len(combined_scores),
        )

    _log_score_ranges(motion_scores, audio_scores, killfeed_scores, combined_scores)
    return combined_scores, kill_counts, death_mask


MOTION_LOOKBACK_SECONDS = 4
MOTION_ONSET_PADDING_SECONDS = 2.0
MOTION_ONSET_CHUNK_SECONDS = 0.5
MOTION_ACTIVITY_THRESHOLD = 0.15


def _expand_events_with_motion(events, motion_scores, fps,
                                max_lookback=MOTION_LOOKBACK_SECONDS,
                                padding=MOTION_ONSET_PADDING_SECONDS,
                                death_mask=None):
    if not events or not motion_scores:
        return events

    norm = normalize_scores(motion_scores)
    max_lookback_frames = int(max_lookback * fps)
    padding_frames = int(padding * fps)
    chunk_frames = max(1, round(fps * MOTION_ONSET_CHUNK_SECONDS))

    expanded = []
    for start_frame, end_frame in events:
        onset = start_frame
        pos = start_frame - chunk_frames

        while pos >= max(0, start_frame - max_lookback_frames):
            end_pos = min(pos + chunk_frames, len(norm))
            chunk = norm[pos:end_pos]
            if not chunk:
                break

            # Stop expansion if this chunk contains a death screen.
            if death_mask and any(death_mask[f] for f in range(pos, end_pos) if f < len(death_mask)):
                LOGGER.debug(
                    "  Event %d-%d: expansion stopped at death screen at frame %d",
                    start_frame, end_frame, pos,
                )
                break

            chunk_avg = sum(chunk) / len(chunk)
            if chunk_avg > MOTION_ACTIVITY_THRESHOLD:
                onset = pos
                pos -= chunk_frames
            else:
                break

        new_start = max(0, onset - padding_frames)
        if new_start < start_frame:
            LOGGER.debug(
                "  Event %d-%d: motion onset at frame %d (%.2fs before event)",
                start_frame, end_frame, onset, (start_frame - onset) / fps,
            )
        expanded.append((new_start, end_frame))

    return expanded


def _trim_events_at_death(
    events: list[tuple[int, int]],
    death_mask: list[bool],
) -> list[tuple[int, int]]:

    if not death_mask:
        return events

    trimmed = []
    for start_frame, end_frame in events:
        # Find the first death frame within this event.
        death_at = None
        for f in range(start_frame, min(end_frame + 1, len(death_mask))):
            if death_mask[f]:
                death_at = f
                break

        if death_at is None:
            # No death screen inside this event — keep unchanged.
            trimmed.append((start_frame, end_frame))
        elif death_at <= start_frame:
            # Event starts on a death frame — discard.
            LOGGER.debug(
                "  Dropping event %d-%d: starts on death frame %d",
                start_frame, end_frame, death_at,
            )
        else:
            new_end = death_at - 1
            LOGGER.debug(
                "  Trimming event %d-%d: death at frame %d, new end %d",
                start_frame, end_frame, death_at, new_end,
            )
            trimmed.append((start_frame, new_end))

    return trimmed

def _extract_audio_safe(video_path, fps, target_length):
    try:
        return extract_audio_scores(video_path, fps, target_length=target_length)
    except Exception:
        LOGGER.exception(
            "Unexpected audio analysis failure for %s. Falling back without audio.",
            video_path,
        )
        return []


def _extract_killfeed_safe(video_path, target_length):
    try:
        result = extract_killfeed_data(video_path, target_length)
        return result.scores, result.kill_counts
    except Exception:
        LOGGER.exception(
            "Unexpected kill-feed analysis failure for %s. Falling back without kill-feed.",
            video_path,
        )
        return [], []


def _extract_death_mask_safe(video_path, target_length):
    try:
        return extract_death_mask(video_path, target_length)
    except Exception:
        LOGGER.exception(
            "Unexpected death-screen analysis failure for %s. Skipping death detection.",
            video_path,
        )
        return []


def _log_score_ranges(motion_scores, audio_scores, killfeed_scores, combined_scores):
    parts = [
        f"motion: {min(motion_scores):.4f}..{max(motion_scores):.4f}",
    ]
    if audio_scores:
        parts.append(f"audio: {min(audio_scores):.4f}..{max(audio_scores):.4f}")
    if killfeed_scores:
        parts.append(f"killfeed: {min(killfeed_scores):.4f}..{max(killfeed_scores):.4f}")
    parts.append(f"combined: {min(combined_scores):.4f}..{max(combined_scores):.4f}")
    LOGGER.info("Score ranges - %s", ", ".join(parts))