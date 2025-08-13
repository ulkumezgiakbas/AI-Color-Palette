
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import cv2
import numpy as np
from sklearn.cluster import KMeans

from ..utils.color import (
    bgr_to_hex,
    bgr_to_rgb,
    clamp,
    harmonies_from_hex,
)
from ..utils.image import decode_image_bytes, resize_long_edge

@dataclass(slots=True)
class ColorInfo:
    rgb: tuple[int, int, int]
    bgr: tuple[int, int, int]
    hex: str
    percent: float
    complements: list[str]
    analogs: list[str]

def extract_palette(
    image_bytes: bytes,
    k: int = 6,
    sample_max: int = 200_000,
) -> tuple[list[ColorInfo], np.ndarray]:
    """
    Extract 'k' dominant colors from an image via KMeans.
    Returns (palette, preview_image_bgr).
    """
    img = decode_image_bytes(image_bytes)  
    if img is None:
        raise ValueError("Görsel açılamadı. jpg/jpeg/png/webp deneyin.")


    preview = resize_long_edge(img, 600)

    pixels = img.reshape(-1, 3)
    if pixels.shape[0] > sample_max:
        idx = np.random.choice(pixels.shape[0], sample_max, replace=False)
        pixels = pixels[idx]

    k = int(clamp(k, 2, 12))
    kmeans = KMeans(n_clusters=k, n_init=8, random_state=42)
    labels = kmeans.fit_predict(pixels)
    centers = kmeans.cluster_centers_.astype(np.uint8)  

    counts = np.bincount(labels, minlength=k)
    percents = counts / counts.sum()

    order = np.argsort(-percents)
    palette: list[ColorInfo] = []
    for i in order:
        bgr = tuple(int(x) for x in centers[i])
        rgb = bgr_to_rgb(bgr)
        hx = bgr_to_hex(bgr)
        complements, analogs = harmonies_from_hex(hx)
        palette.append(
            ColorInfo(
                rgb=rgb,
                bgr=bgr,
                hex=hx,
                percent=float(percents[i]),
                complements=complements,
                analogs=analogs,
            )
        )

    return palette, preview
