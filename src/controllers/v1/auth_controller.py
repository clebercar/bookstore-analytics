import os
from datetime import datetime, timedelta, timezone

import jwt
from flasgger import swag_from
from flask import Blueprint, jsonify, request
from pydantic import BaseModel, EmailStr, ValidationError, constr

from src.db.connection import db_connection_handler
from src.repositories.user_repository import UserRepository

auth_controller = Blueprint("auth_controller", __name__)


def generate_token(user_id: int):
    secret_key = os.getenv("SECRET_KEY")

    return jwt.encode(
        {"user_id": user_id, "exp": datetime.now(timezone.utc) + timedelta(minutes=30)},
        secret_key,
        algorithm="HS256",
    )


@auth_controller.route("/api/v1/auth/login", methods=["POST"])
@swag_from(
    {
        "tags": ["auth"],
        "summary": "User login",
        "description": "Authenticate user and return JWT token.",
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "example": "user@example.com"},
                        "password": {"type": "string", "example": "password123"},
                    },
                    "required": ["email", "password"],
                },
            }
        ],
        "responses": {
            200: {
                "description": "JWT token returned",
                "schema": {
                    "type": "object",
                    "properties": {"token": {"type": "string"}},
                },
            },
            400: {"description": "Validation error"},
            401: {"description": "Authentication failed"},
        },
    }
)
def auth_login():
    try:
        data = request.get_json()

        validated_data = validate_sign_in_data(data)

        user_repository = UserRepository(db_connection_handler)
        user = user_repository.get_user_by_email_and_password(
            validated_data.email, validated_data.password
        )

        if not user:
            return jsonify({"error": "Occurred an error while signing in"}), 401

        token = generate_token(user.id)

        return jsonify({"token": token}), 200
    except (ValidationError, ValueError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def validate_sign_in_data(user_data):
    class SignInData(BaseModel):
        email: EmailStr
        password: constr(min_length=8)  # type: ignore

    try:
        return SignInData(**user_data)
    except ValidationError as e:
        raise ValueError(str(e))


@auth_controller.route("/api/v1/auth/refresh", methods=["POST"])
@swag_from(
    {
        "tags": ["auth"],
        "summary": "Refresh JWT token",
        "description": "Refresh and return a new JWT token.",
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "token": {"type": "string", "example": "<jwt_token>"}
                    },
                    "required": ["token"],
                },
            }
        ],
        "responses": {
            200: {
                "description": "New JWT token returned",
                "schema": {
                    "type": "object",
                    "properties": {"token": {"type": "string"}},
                },
            },
            400: {"description": "Token missing or invalid"},
            403: {"description": "Invalid token"},
        },
    }
)
def refresh_token():
    try:
        secret_key = os.getenv("SECRET_KEY")

        data = request.get_json()
        token = data.get("token")

        if not token:
            return jsonify({"error": "Token is required"}), 400

        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])

        return jsonify({"token": generate_token(decoded_token["user_id"])}), 200
    except jwt.InvalidTokenError:
        return jsonify(message="invalid token"), 403
