from flasgger import swag_from
from flask import Blueprint, jsonify

health_controller = Blueprint("health_controller", __name__)


@health_controller.route("/api/v1/health", methods=["GET"])
@swag_from(
    {
        "tags": ["health"],
        "summary": "Health check endpoint",
        "description": "Returns a simple OK response to verify the service is running.",
        "responses": {
            200: {
                "description": "Service is healthy",
                "schema": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "example": "OK"},
                        "message": {"type": "string", "example": "Service is healthy"},
                    },
                },
            }
        },
    }
)
def health():
    """
    Health check endpoint

    Returns a simple OK response to verify the service is running.
    """
    return jsonify({"status": "OK", "message": "Service is healthy"})
