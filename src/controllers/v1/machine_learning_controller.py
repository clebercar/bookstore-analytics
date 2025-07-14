from flasgger import swag_from
from flask import Blueprint, jsonify, request

from src.db.connection import db_connection_handler
from src.ml.predict_service import predict_stars
from src.repositories.books_repository import BooksRepository

machine_learning_controller = Blueprint("machine_learning_controller", __name__)


@machine_learning_controller.route("/api/v1/ml/features", methods=["GET"])
@swag_from(
    {
        "tags": ["ml"],
        "summary": "Get machine learning features",
        "description": "Returns the features used for machine learning model training.",
        "responses": {
            200: {
                "description": "Machine learning features",
                "schema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "price": {"type": "number"},
                            "category": {"type": "string"},
                            "stars": {"type": "integer"},
                        },
                    },
                },
            },
            500: {"description": "Internal Server Error"},
        },
    }
)
def features():
    """
    Get machine learning features

    Returns the features used for machine learning model training.
    """
    books_repository = BooksRepository(db_connection_handler)
    books = books_repository.get_books_features()

    return jsonify(books)


@machine_learning_controller.route("/api/v1/ml/training-data", methods=["GET"])
@swag_from(
    {
        "tags": ["ml"],
        "summary": "Get training data",
        "description": "Returns the data used to train the machine learning model.",
        "responses": {
            200: {
                "description": "Training data",
                "schema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "price": {"type": "number"},
                            "category": {"type": "string"},
                            "stars": {"type": "integer"},
                        },
                    },
                },
            },
            500: {"description": "Internal Server Error"},
        },
    }
)
def training_data():
    """
    Get training data

    Returns the data used to train the machine learning model.
    """
    books_repository = BooksRepository(db_connection_handler)
    books = books_repository.get_training_data()

    return jsonify(books)


@machine_learning_controller.route("/api/v1/ml/predictions", methods=["POST"])
@swag_from(
    {
        "tags": ["ml"],
        "summary": "Predict book rating",
        "description": "Predicts the rating (1-5 stars) for a book based on its price and category.",
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "price": {
                            "type": "number",
                            "description": "Book price",
                            "required": True,
                        },
                        "category": {
                            "type": "string",
                            "description": "Book category",
                            "required": True,
                        },
                    },
                },
            }
        ],
        "responses": {
            200: {
                "description": "Prediction result",
                "schema": {
                    "type": "object",
                    "properties": {
                        "predicted_stars": {
                            "type": "number",
                            "description": "Predicted rating (1-5 stars)",
                        }
                    },
                },
            },
            400: {
                "description": "Bad Request - Missing required fields",
                "schema": {
                    "type": "object",
                    "properties": {
                        "error": {"type": "string", "description": "Error message"}
                    },
                },
            },
            500: {"description": "Internal Server Error"},
        },
    }
)
def predict():
    """
    Predict book rating

    Predicts the rating (1-5 stars) for a book based on its price and category.
    """
    try:
        data = request.get_json()
        if not data or "price" not in data or "category" not in data:
            return (
                jsonify({"error": "Campos 'price' e 'category' são obrigatórios."}),
                400,
            )

        prediction = predict_stars(data)

        return jsonify({"predicted_stars": prediction})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
