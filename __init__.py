from __future__ import annotations

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app() -> Flask:
    """
    Factory to create and configure the Flask application.
    - Registers blueprints
    - Applies sane defaults for JSON and security headers
    """
    app = Flask(__name__)
    app.config.update(
        JSON_AS_ASCII=False,
        JSON_SORT_KEYS=False,
        MAX_CONTENT_LENGTH=10 * 1024 * 1024,  # 10MB upload limit
    )

   
    from .blueprints.palette import bp as palette_bp
    app.register_blueprint(palette_bp)


    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  

    @app.after_request
    def _add_headers(resp):
        resp.headers.setdefault("X-Content-Type-Options", "nosniff")
        resp.headers.setdefault("X-Frame-Options", "DENY")
        resp.headers.setdefault("Referrer-Policy", "no-referrer")
        return resp

    return app
