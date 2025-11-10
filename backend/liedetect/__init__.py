from flask import Flask
from flask_cors import CORS
import logging
import os

from .config import settings
from .routes.media import media_bp
from .routes.inference import inference_bp


logger = logging.getLogger("liedetect")


def create_app() -> Flask:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    app = Flask(__name__)
    app.config.from_mapping(settings.to_flask_config())
    CORS(app, resources={r"/*": {"origins": settings.allowed_origins or "*"}})

    app.register_blueprint(media_bp)
    app.register_blueprint(inference_bp)

    @app.get("/health")
    def health_check():
        return {"status": "ok", "environment": settings.env}

    logger.info("LieDetect backend initialized", extra={"env": settings.env})
    return app
