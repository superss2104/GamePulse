DEFAULT_CLIP_LEN_SECONDS = 4
DEFAULT_START_BIAS_SECONDS = -2.0
DEFAULT_MIN_CLIP_GAP_SECONDS = 0


DEFAULT_END_BIAS_SECONDS = 2.0


def frames_to_timestamps(
    merged_windows,
    fps,
    clip_len=DEFAULT_CLIP_LEN_SECONDS,
    start_bias=DEFAULT_START_BIAS_SECONDS,
    end_bias=DEFAULT_END_BIAS_SECONDS,
    death_mask=None,
):
    timestamps = []

    for start_frame, end_frame in merged_windows:
        target_start_frame = max(0, start_frame + int(start_bias * fps))
        
        # Clamp start_frame backward to avoid death screens before the event
        if death_mask:
            for f in range(end_frame, target_start_frame - 1, -1):
                if f < len(death_mask) and death_mask[f]:
                    target_start_frame = f + 1
                    break

        event_duration_frames = end_frame - target_start_frame
        target_clip_len_frames = int(clip_len * fps)
        
        if event_duration_frames <= target_clip_len_frames:
            target_end_frame = target_start_frame + target_clip_len_frames
        else:
            target_end_frame = end_frame + int(end_bias * fps)

        # Clamp end_frame forward to avoid death screens after the event
        if death_mask:
            for f in range(end_frame + 1, min(target_end_frame + 1, len(death_mask))):
                if death_mask[f]:
                    target_end_frame = f - 1
                    break
            target_end_frame = min(target_end_frame, len(death_mask) - 1)
            
        clip_start = target_start_frame / fps
        clip_end = max(target_end_frame, target_start_frame) / fps

        timestamps.append((clip_start, clip_end))

    return timestamps


def merge_overlapping_clips(timestamps, min_gap=DEFAULT_MIN_CLIP_GAP_SECONDS):
    if not timestamps:
        return []

    sorted_timestamps = sorted(timestamps) #to ensure they're chronologically sorted
    merged = [sorted_timestamps[0]]

    for start, end in sorted_timestamps[1:]:
        last_start, last_end = merged[-1] #previous start and end
        if start <= last_end + min_gap:
            merged[-1] = (last_start, max(last_end, end)) #if the new clip starts before the previous clip ends plus a small gap, merge them
        else:
            merged.append((start, end))

    return merged


