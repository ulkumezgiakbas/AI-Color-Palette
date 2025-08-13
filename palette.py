
from __future__ import annotations

from typing import Any, Dict
from flask import Blueprint, jsonify, render_template, request

from ..services.palette_service import extract_palette
from ..utils.image import image_to_data_url

bp = Blueprint("palette", __name__)

@bp.get("/")
def index() -> str:
    return render_template("index.html")

@bp.post("/api/extract")
def api_extract():
    """Extract a color palette from an uploaded image (file or raw body)."""
    try:
        k_raw = request.form.get("k", request.args.get("k", "6"))
        k = int(k_raw) if k_raw else 6

        if "image" in request.files:
            data = request.files["image"].read()
        else:
            
            data = request.get_data()
            if not data:
                return jsonify({"error": "Görsel yüklenmedi."}), 400

        palette, preview = extract_palette(data, k=k)
        payload: Dict[str, Any] = {
            "preview": image_to_data_url(preview),
            "colors": [
                {
                    "hex": c.hex,
                    "rgb": c.rgb,
                    "percent": round(c.percent * 100, 2),
                    "complements": c.complements,
                    "analogs": c.analogs,
                }
                for c in palette
            ],
        }
        return jsonify(payload)
    except Exception as exc:  
        return jsonify({"error": str(exc)}), 400
