from flask import Blueprint, jsonify, request

from src.db.connection import db_connection_handler
from src.ml.predict_service import predict_stars
from src.repositories.books_repository import BooksRepository

machine_learning_controller = Blueprint("machine_learning_controller", __name__)


@machine_learning_controller.route("/api/v1/ml/features", methods=["GET"])
def features():
    books_repository = BooksRepository(db_connection_handler)
    books = books_repository.get_books_features()

    return jsonify(books)


@machine_learning_controller.route("/api/v1/ml/training-data", methods=["GET"])
def training_data():
    books_repository = BooksRepository(db_connection_handler)
    books = books_repository.get_training_data()

    return jsonify(books)


@machine_learning_controller.route("/api/v1/ml/predictions", methods=["POST"])
def predict():
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
