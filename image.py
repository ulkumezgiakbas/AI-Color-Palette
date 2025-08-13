
from __future__ import annotations

import base64
import cv2
import numpy as np

def decode_image_bytes(image_bytes: bytes):
    """Decode raw bytes into a BGR image using OpenCV."""
    file_bytes = np.frombuffer(image_bytes, np.uint8)
    return cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

def resize_long_edge(img_bgr, target: int):
    """Resize preserving aspect ratio so that the long edge equals `target`."""
    h, w = img_bgr.shape[:2]
    scale = target / max(h, w)
    if scale < 1.0:
        new_size = (int(w * scale), int(h * scale))
        return cv2.resize(img_bgr, new_size, interpolation=cv2.INTER_AREA)
    return img_bgr.copy()

def image_to_data_url(img_bgr) -> str:
    ok, buf = cv2.imencode(".jpg", img_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 88])
    if not ok:
        return ""
    b64 = base64.b64encode(buf.tobytes()).decode("ascii")
    return f"data:image/jpeg;base64,{b64}"
