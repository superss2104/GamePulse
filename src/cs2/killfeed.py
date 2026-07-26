import logging
from dataclasses import dataclass, field


import cv2
import numpy as np

LOGGER = logging.getLogger(__name__)

@dataclass
class KillfeedConfig:

    #Region of Interest Bounds as fractions of the entire screen
    roi_x_start: float = 0.7
    roi_y_start: float = 0.01
    roi_x_end: float = 1
    roi_y_end: float = 0.35

    #Red wraps around the hue wheel so we need two ranges
    red_hue_low: tuple = (0, 100, 100) #(Hue, Sat, Val)
    red_hue_low_upper: tuple = (10, 255, 255)
    red_hue_high: tuple = (170, 100, 100)
    red_hue_high_upper: tuple = (180, 255, 255)

    #minm size of killfeed entry as fraction of ROI
    min_area_ratio: float = 0.005

    #minm aspect ratio (width / height) for a valid kill-feed rectangle
    min_aspect_ratio: float = 2.0

    #Prevent deathscreens from being detected as a killfeed
    max_interior_fill: float = 0.30

    #Prevent deaths from being counted
    max_inner_fill: float = 0.10

    #Ignore the border of the killfeed rectangle while detecting red pixels
    border_zone_ratio: float = 0.15

    # Polygon approximation tolerance (fraction of perimeter).
    approx_epsilon: float = 0.04

    # maxm number of vertices after polygon approximation. Rectangles with
    # slightly rounded corners may produce 4-8 vertices.
    max_vertices: int = 8

    # Multi-kill score cap to prevent the supression of other highlights.
    max_score: float = 3.0


DEFAULT_CONFIG = KillfeedConfig()

@dataclass
class KillfeedResult:
    scores: list[float] = field(default_factory=list) # Ensures a new list is created each time the class is instantiated
    kill_counts: list[int] = field(default_factory=list)

def extract_killfeed_data(video_path, target_length, config=None):
    if target_length <= 0:
        return KillfeedResult()

    if config is None:
        config = DEFAULT_CONFIG

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        LOGGER.warning("Kill-feed detection: failed to open video %s", video_path)
        return KillfeedResult()

    try:
        raw_scores = []
        raw_counts = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            score, count = detect_player_kills_detailed(frame, config)
            raw_scores.append(score)
            raw_counts.append(count)
    finally:
        cap.release()

    if not raw_scores:
        return KillfeedResult()

    aligned_scores = _align_scores(raw_scores, target_length)
    aligned_counts = _align_counts(raw_counts, target_length)
    LOGGER.info("Extracted %d kill-feed scores (max %.2f)", len(aligned_scores), max(aligned_scores))
    return KillfeedResult(scores=aligned_scores, kill_counts=aligned_counts)



def detect_player_kills_detailed(frame, config=None):
    if config is None:
        config = DEFAULT_CONFIG

    h, w = frame.shape[:2]
    roi = _crop_roi(frame, w, h, config)
    roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV) #Converts the Region Of Interest to HSV Color space
    red_mask = _build_red_mask(roi_hsv, config) #Binary mask for red pixels

    outlines = find_red_outlines(red_mask, config)
    count = len(outlines) #counts detected kill feed entries

    if count == 0:
        return 0.0, 0
    # First kill = 1.0, each additional adds 0.5, capped.
    score = min(1.0 + 0.5 * (count - 1), config.max_score)
    return score, count



def _crop_roi(frame, frame_w, frame_h, config):
    x1 = int(frame_w * config.roi_x_start)
    y1 = int(frame_h * config.roi_y_start)
    x2 = int(frame_w * config.roi_x_end)
    y2 = int(frame_h * config.roi_y_end)
    return frame[y1:y2, x1:x2]


def _build_red_mask(hsv_roi, config):
    #Create a binary mask of red-hue pixels in the ROI
    mask_low = cv2.inRange(
        hsv_roi,
        np.array(config.red_hue_low, dtype=np.uint8),
        np.array(config.red_hue_low_upper, dtype=np.uint8),
    )
    mask_high = cv2.inRange(
        hsv_roi,
        np.array(config.red_hue_high, dtype=np.uint8),
        np.array(config.red_hue_high_upper, dtype=np.uint8),
    )
    return cv2.bitwise_or(mask_low, mask_high)


def find_red_outlines(red_mask, config):
    # Apply a small morphological close to bridge micro-gaps caused by chroma subsampling
    # But only horizontal! A (1, 5) kernel bridges broken walls without bridging stacked kills!
    kernel = np.ones((1, 5), np.uint8)
    closed_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(closed_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    roi_h, roi_w = red_mask.shape[:2]
    roi_area = roi_h * roi_w
    min_area = roi_area * config.min_area_ratio

    # A typical single killfeed is ~10% of the ROI height (if ROI is 0.35 of screen)
    expected_kill_height = roi_h * 0.10

    valid = []
    for contour in contours:
        if is_hollow_rectangle(contour, red_mask, min_area, config):
            valid.append(contour)
        else:
            # MULTIKILL FALLBACK
            # If the contour failed the strict single-rectangle check, it might be a 
            # massive stair-stepped blob of stacked multikills!
            x, y, w, h = cv2.boundingRect(contour)
            bbox_area = w * h
            
            # If it's a massive blob that is wide enough to be a killfeed
            if bbox_area > min_area * 1.5 and w > expected_kill_height * 3:
                # Estimate kills conservatively. A 2-kill stack will have height ~ 2.0x
                # A single kill with noise might reach 1.4x. We don't want 1.5 to round up to 2.
                ratio = h / expected_kill_height
                estimated_kills = max(1, int(ratio + 0.25))
                
                # Verify that it's mostly hollow (multikills are just stacked hollow rectangles)
                interior = red_mask[y:y+h, x:x+w]
                fill_ratio = np.count_nonzero(interior) / max(1, interior.size)
                
                if estimated_kills > 1 and fill_ratio < 0.40:
                    # Duplicate the contour in the list so that len(valid) increases by the kill count!
                    for _ in range(estimated_kills):
                        valid.append(contour)

    return valid

def is_hollow_rectangle(contour, red_mask, min_area, config):
    # Use bounding box area instead of raw contour area.
    # A broken contour has almost 0 area, but its bounding box still perfectly covers the killfeed!
    x, y, w, h = cv2.boundingRect(contour)
    if h == 0 or w == 0:
        return False
        
    bbox_area = w * h
    if bbox_area < min_area:
        return False

    aspect = w / h
    if aspect < config.min_aspect_ratio:
        return False

    # Check if the overall box isn't just a solid block (e.g. death screen)
    interior = red_mask[y:y + h, x:x + w]
    if interior.size == 0:
        return False

    fill_ratio = np.count_nonzero(interior) / interior.size
    if fill_ratio > config.max_interior_fill:
        return False

    # Check if the INNER core is completely hollow (no red pixels inside)
    border = max(4, int(min(w, h) * config.border_zone_ratio))
    inner_y1 = y + border
    inner_y2 = y + h - border
    inner_x1 = x + border
    inner_x2 = x + w - border

    if inner_y2 > inner_y1 and inner_x2 > inner_x1:
        inner = red_mask[inner_y1:inner_y2, inner_x1:inner_x2]
        if inner.size > 0:
            inner_fill = np.count_nonzero(inner) / inner.size
            if inner_fill > config.max_inner_fill:
                return False

    return True


def _align_scores(raw_scores, target_length):
   
    n = len(raw_scores)
    if n == target_length:
        return raw_scores
    if n == 0:
        return [0.0] * target_length

    aligned = []
    for i in range(target_length):
        src_idx = round(i * (n - 1) / max(1, target_length - 1))
        src_idx = min(src_idx, n - 1) #to avoid rounding off at n (out of bounds)
        aligned.append(raw_scores[src_idx])
    return aligned


def _align_counts(raw_counts, target_length):
    n = len(raw_counts)
    if n == target_length:
        return raw_counts
    if n == 0:
        return [0] * target_length

    aligned = []
    for i in range(target_length):
        src_idx = round(i * (n - 1) / max(1, target_length - 1))
        src_idx = min(src_idx, n - 1)
        aligned.append(raw_counts[src_idx])
    return aligned