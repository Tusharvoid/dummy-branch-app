from flask import Flask
import logging
import sys
import os
from prometheus_flask_exporter import PrometheusMetrics

from .config import Config

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config())

    # Configure Logging
    log_format = os.getenv("LOG_FORMAT", "text")
    if log_format == "json":
        # Simple JSON logging setup
        class JsonFormatter(logging.Formatter):
            def format(self, record):
                import json
                log_record = {
                    "level": record.levelname,
                    "message": record.getMessage(),
                    "time": self.formatTime(record, self.datefmt),
                    "name": record.name
                }
                if record.exc_info:
                    log_record["exception"] = self.formatException(record.exc_info)
                return json.dumps(log_record)

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)
    else:
        logging.basicConfig(level=logging.INFO)

    # Initialize Prometheus Metrics
    metrics = PrometheusMetrics(app)
    metrics.info('app_info', 'Application info', version='1.0.0')

    # Lazy imports to avoid circular deps during app init
    from .routes.health import bp as health_bp
    from .routes.loans import bp as loans_bp
    from .routes.stats import bp as stats_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(loans_bp, url_prefix="/api")
    app.register_blueprint(stats_bp, url_prefix="/api")

    return app
