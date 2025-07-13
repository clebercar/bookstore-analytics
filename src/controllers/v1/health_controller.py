from flask import Blueprint

health_controller = Blueprint("health_controller", __name__)


@health_controller.route("/api/v1/health", methods=["GET"])
def health():
    return "OK"
