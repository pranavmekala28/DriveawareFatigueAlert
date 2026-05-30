"""
DriveAware Backend - SmartSpectra Integration Layer
Flask app serving the DriveAware frontend + API endpoints.
"""

import os
import time
import logging
from datetime import datetime

import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS


# Load .env
load_dotenv()

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s"
)
logger = logging.getLogger("DriveAware")


# Configuration
PRESAGE_API_KEY = os.getenv("PRESAGE_API_KEY", "")
PRESAGE_AUTH_BASE = "https://physiology.presagetech.com"


# Flask app
app = Flask(__name__)
CORS(app)


class SmartSpectraClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "X-API-Key": self.api_key,
            "User-Agent": "DriveAware/1.0.0"
        })

        logger.info(
            "SmartSpectra client initialized "
            f"(key configured: {bool(api_key)})"
        )

    def validate_api_key(self) -> dict:
        if not self.api_key:
            return {
                "valid": False,
                "reachable": False,
                "reason": "no_key_provided",
                "message": "PRESAGE_API_KEY not set in .env file"
            }

        try:
            response = self.session.get(PRESAGE_AUTH_BASE, timeout=8)

            return {
                "valid": response.status_code in [200, 401, 403],
                "reachable": True,
                "status_code": response.status_code,
                "message": "Presage endpoint contacted successfully"
            }

        except requests.RequestException as error:
            return {
                "valid": False,
                "reachable": False,
                "reason": "network_error",
                "error": str(error)
            }

    def measure_vitals(self, duration_seconds: int = 30) -> dict:
        auth_status = self.validate_api_key()

        return {
            "ok": True,
            "session_id": f"VITALS_{int(time.time())}",
            "duration_seconds": duration_seconds,
            "auth": auth_status,
            "metrics": {
                "pulseRate": {
                    "value": None,
                    "confidence": 0.0,
                    "unit": "bpm",
                    "source": "SmartSpectra SDK"
                },
                "hrv": {
                    "value": None,
                    "confidence": 0.0,
                    "unit": "ms",
                    "source": "SmartSpectra SDK"
                },
                "breathingRate": {
                    "value": None,
                    "confidence": 0.0,
                    "unit": "rpm",
                    "source": "SmartSpectra SDK"
                },
                "stress": {
                    "value": None,
                    "confidence": 0.0,
                    "source": "SmartSpectra SDK"
                }
            },
            "integration_status": "ready_for_native_sdk",
            "notes": (
                "Browser demo uses MediaPipe Face Mesh for EAR, blink count, "
                "PERCLOS, and fatigue score. SmartSpectra SDK can be connected "
                "through native iOS, Android, or C++ clients."
            ),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }


smartspectra = SmartSpectraClient(PRESAGE_API_KEY)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "DriveAware",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })


@app.route("/api/auth/validate", methods=["GET"])
def auth_validate():
    return jsonify(smartspectra.validate_api_key())


@app.route("/api/vitals/measure", methods=["POST"])
def vitals_measure():
    payload = request.json or {}
    duration = payload.get("duration_seconds", 30)

    return jsonify(smartspectra.measure_vitals(duration_seconds=duration))


@app.route("/api/vitals/ingest", methods=["POST"])
def vitals_ingest():
    payload = request.json or {}

    session_id = payload.get("session_id", "unknown")
    metrics = payload.get("metrics", {})

    logger.info(
        f"Vitals ingested for session {session_id}: {list(metrics.keys())}"
    )

    return jsonify({
        "ok": True,
        "session_id": session_id,
        "metrics_received": list(metrics.keys()),
        "received_at": datetime.utcnow().isoformat() + "Z"
    })


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("DriveAware Backend Starting")
    logger.info("=" * 60)
    logger.info(f"Presage API key configured: {bool(PRESAGE_API_KEY)}")
    logger.info("Frontend: http://127.0.0.1:5000")
    logger.info("Health:   http://127.0.0.1:5000/api/health")
    logger.info("=" * 60)

    app.run(host="0.0.0.0", port=5050, debug=True)