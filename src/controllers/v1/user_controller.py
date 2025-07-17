from flask import Blueprint, jsonify, request
from pydantic import BaseModel, EmailStr, ValidationError, constr

from src.db.connection import db_connection_handler
from src.models.user import User
from src.repositories.user_repository import UserRepository

user_controller = Blueprint("user_controller", __name__)


@user_controller.route("/api/v1/users", methods=["POST"])
def create_user():
    try:
        user_data = request.get_json()

        validated_data = validate_user_data(user_data)

        user = User(
            name=validated_data.name,
            email=validated_data.email,
            password=validated_data.password,
        )

        user_repository = UserRepository(db_connection_handler)
        user_repository.create_user(user)

        return jsonify({}), 201
    except (ValidationError, ValueError) as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def validate_user_data(user_data):
    class UserData(BaseModel):
        name: constr(min_length=3)  # type: ignore
        email: EmailStr
        password: constr(min_length=8)  # type: ignore
        confirm_password: constr(min_length=8)  # type: ignore

    try:
        validated_data = UserData(**user_data)
        if validated_data.password != validated_data.confirm_password:
            raise ValueError("Passwords do not match")

        return validated_data
    except ValidationError as e:
        raise ValueError(str(e))
    except ValueError as e:
        raise e
