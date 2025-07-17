from flasgger import swag_from
from flask import Blueprint, jsonify

from src.db.connection import db_connection_handler
from src.repositories.categories_repository import CategoriesRepository

categories_controller = Blueprint("categories_controller", __name__)


@categories_controller.route("/api/v1/categories", methods=["GET"])
@swag_from(
    {
        "tags": ["categories"],
        "summary": "List all categories",
        "description": "Returns a list of all available book categories.",
        "responses": {
            200: {
                "description": "List of categories",
                "schema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "Unique category ID",
                            },
                            "name": {"type": "string", "description": "Category name"},
                        },
                    },
                },
            },
            500: {"description": "Internal Server Error"},
        },
    }
)
def list_categories():
    """
    List all categories

    Returns a list of all available book categories.
    """
    categories_repository = CategoriesRepository(db_connection_handler)
    categories = categories_repository.list_categories()

    return jsonify(categories)
