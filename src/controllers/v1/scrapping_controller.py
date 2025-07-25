import os
import threading

import jwt
from flasgger import swag_from
from flask import Blueprint, jsonify, request

from src.scripts.scrapper import scrapper

scrapping_controller = Blueprint("scrapping_controller", __name__)


@scrapping_controller.route("/api/v1/scrapping/trigger", methods=["POST"])
@swag_from(
    {
        "tags": ["scrapping"],
        "summary": "Trigger scrapping process",
        "description": "Triggers the scrapping process. Requires JWT token in Authorization header.",
        "parameters": [
            {
                "name": "Authorization",
                "in": "header",
                "type": "string",
                "required": True,
                "description": "JWT token in the format: Bearer <token>",
            }
        ],
        "responses": {
            202: {"description": "Scrapping triggered"},
            401: {"description": "Token expired"},
            403: {"description": "Token missing or invalid"},
        },
    }
)
def trigger_scrapping():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify(message="Token is required"), 403

    parts = auth_header.split()
    token = parts[1]

    try:
        jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])

        thread = threading.Thread(target=scrapper)
        thread.start()

        return jsonify(message="Scrapping triggered"), 202
    except jwt.ExpiredSignatureError:
        return jsonify(message="Token expired! Please login again."), 401
    except jwt.InvalidTokenError:
        return jsonify(message="Invalid token!"), 403
