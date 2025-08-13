
from __future__ import annotations

import cv2
import numpy as np

def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))

def bgr_to_hex(bgr: tuple[int, int, int]) -> str:
    b, g, r = bgr
    return f"#{r:02X}{g:02X}{b:02X}"

def bgr_to_rgb(bgr: tuple[int, int, int]) -> tuple[int, int, int]:
    b, g, r = bgr
    return (r, g, b)

def hex_to_bgr(hx: str) -> tuple[int, int, int]:
    hx = hx.lstrip("#")
    r = int(hx[0:2], 16)
    g = int(hx[2:4], 16)
    b = int(hx[4:6], 16)
    return (b, g, r)

def _hsv_to_hex(hsv_trip: tuple[int, int, int]) -> str:
    arr = np.uint8([[[
        int(clamp(hsv_trip[0], 0, 179)),
        int(clamp(hsv_trip[1], 0, 255)),
        int(clamp(hsv_trip[2], 0, 255)),
    ]]])
    bgr = cv2.cvtColor(arr, cv2.COLOR_HSV2BGR)[0, 0]
    return bgr_to_hex(tuple(int(x) for x in bgr))

def harmonies_from_hex(hx: str) -> tuple[list[str], list[str]]:
    """
    Compute simple color harmonies based on HSV hue rotations:
    - Complementary: +180°  (OpenCV hue range 0..179 -> +90)
    - Analogs: ±30°         (OpenCV hue units ~ half-degree; use ±15)
    Returns (complements, analogs) both as HEX strings.
    """
   
    b, g, r = hex_to_bgr(hx)
    hsv = cv2.cvtColor(np.uint8([[[b, g, r]]]), cv2.COLOR_BGR2HSV)[0, 0]
    h, s, v = [int(x) for x in hsv]

    comp_h = (h + 90) % 180  # ≈ +180°
    a1 = (h + 15) % 180      # ≈ +30°
    a2 = (h - 15) % 180      # ≈ -30°

    complements = [_hsv_to_hex((comp_h, s, v))]
    analogs = [_hsv_to_hex((a1, s, v)), _hsv_to_hex((a2, s, v))]
    return complements, analogs
