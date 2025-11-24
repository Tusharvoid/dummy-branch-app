from flask import Blueprint, jsonify
from app.db import engine
from sqlalchemy import text

bp = Blueprint("health", __name__)

@bp.route("/health", methods=["GET"])
def health():
    try:
        # Check database connectivity
        with engine.connect() as connection:
            connection.execute(text('SELECT 1'))
        return jsonify({"status": "ok", "database": "connected"})
    except Exception as e:
        return jsonify({"status": "error", "database": "disconnected", "error": str(e)}), 500
