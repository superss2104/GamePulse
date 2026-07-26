import logging

import cv2
import numpy as np

LOGGER = logging.getLogger(__name__)

# Mean brightness threshold (0-255).  Frames whose centre brightness is
# below this value are classified as death screens.
DEATH_BRIGHTNESS_THRESHOLD = 15

# Central ROI bounds as fractions of the frame dimensions.
# Avoids HUD elements at the very top and bottom edges.
_ROI_X0, _ROI_X1 = 0.30, 0.70
_ROI_Y0, _ROI_Y1 = 0.30, 0.70


def is_death_frame(frame: np.ndarray) -> bool:
    h, w = frame.shape[:2]
    x0, x1 = int(w * _ROI_X0), int(w * _ROI_X1)
    y0, y1 = int(h * _ROI_Y0), int(h * _ROI_Y1)
    roi = frame[y0:y1, x0:x1]
    if roi.size == 0:
        return False
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    return float(gray.mean()) < DEATH_BRIGHTNESS_THRESHOLD


def extract_death_mask(video_path: str, target_length: int) -> list[bool]:
    if target_length <= 0:
        return []

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        LOGGER.warning("Death-screen detector: failed to open %s", video_path)
        return [False] * target_length

    try:
        raw: list[bool] = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            raw.append(is_death_frame(frame))
    finally:
        cap.release()

    if not raw:
        return [False] * target_length

    death_count = sum(raw)
    LOGGER.info(
        "Death-screen detector: %d / %d raw frames classified as death screens",
        death_count, len(raw),
    )

    # Align to target_length via nearest-neighbour resampling.
    n = len(raw)
    if n == target_length:
        return raw

    aligned: list[bool] = []
    for i in range(target_length):
        src = round(i * (n - 1) / max(1, target_length - 1))
        aligned.append(raw[min(src, n - 1)])

    LOGGER.info(
        "Death-screen detector: %d death frames after alignment to %d frames",
        sum(aligned), target_length,
    )
    return aligned
