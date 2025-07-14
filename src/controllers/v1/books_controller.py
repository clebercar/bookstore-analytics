from flasgger import swag_from
from flask import Blueprint, jsonify, request

from src.db.connection import db_connection_handler
from src.repositories.books_repository import BooksRepository

books_controller = Blueprint("books_controller", __name__)


@books_controller.route("/api/v1/books", methods=["GET"])
@swag_from(
    {
        "tags": ["books"],
        "summary": "List all books",
        "description": "Returns a list of books with optional filtering by title and category.",
        "parameters": [
            {
                "name": "title",
                "in": "query",
                "type": "string",
                "required": False,
                "description": "Filter books by title",
            },
            {
                "name": "category",
                "in": "query",
                "type": "string",
                "required": False,
                "description": "Filter books by category",
            },
        ],
        "responses": {
            200: {
                "description": "List of books",
                "schema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "title": {"type": "string"},
                            "author": {"type": "string"},
                            "price": {"type": "number"},
                            "stars": {"type": "integer"},
                            "category_id": {"type": "integer"},
                            "category_name": {"type": "string"},
                            "url": {"type": "string"},
                            "image_url": {"type": "string"},
                        },
                    },
                },
            },
            500: {"description": "Internal Server Error"},
        },
    }
)
def list_books():
    """
    List all books

    Returns a list of books with optional filtering by title and category.
    """
    title = request.args.get("title")
    category = request.args.get("category")

    books_repository = BooksRepository(db_connection_handler)
    books = books_repository.list_books(title=title, category=category)

    return jsonify(books)


@books_controller.route("/api/v1/books/<string:book_id>", methods=["GET"])
@swag_from(
    {
        "tags": ["books"],
        "summary": "Get a specific book by ID",
        "description": "Returns detailed information about a specific book.",
        "parameters": [
            {
                "name": "book_id",
                "in": "path",
                "type": "string",
                "required": True,
                "description": "The book ID",
            }
        ],
        "responses": {
            200: {
                "description": "Book details",
                "schema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "title": {"type": "string"},
                        "author": {"type": "string"},
                        "price": {"type": "number"},
                        "stars": {"type": "integer"},
                        "category_id": {"type": "integer"},
                        "category_name": {"type": "string"},
                        "url": {"type": "string"},
                        "image_url": {"type": "string"},
                    },
                },
            },
            404: {"description": "Book not found"},
            500: {"description": "Internal Server Error"},
        },
    }
)
def get_book_by_id(book_id):
    """
    Get a specific book by ID

    Returns detailed information about a specific book.
    """
    books_repository = BooksRepository(db_connection_handler)
    book = books_repository.get_book_by_id(book_id)

    if not book:
        return jsonify({"error": "Book not found"}), 404

    return jsonify(book)


@books_controller.route("/api/v1/books/top-rated", methods=["GET"])
@swag_from(
    {
        "tags": ["books"],
        "summary": "Get top rated books",
        "description": "Returns a list of books sorted by rating (highest first).",
        "responses": {
            200: {
                "description": "List of top rated books",
                "schema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "title": {"type": "string"},
                            "author": {"type": "string"},
                            "price": {"type": "number"},
                            "stars": {"type": "integer"},
                            "category_id": {"type": "integer"},
                            "category_name": {"type": "string"},
                            "url": {"type": "string"},
                            "image_url": {"type": "string"},
                        },
                    },
                },
            },
            500: {"description": "Internal Server Error"},
        },
    }
)
def top_rated_books():
    """
    Get top rated books

    Returns a list of books sorted by rating (highest first).
    """
    books_repository = BooksRepository(db_connection_handler)
    books = books_repository.top_rated_books()

    return jsonify(books)


@books_controller.route("/api/v1/books/price-range", methods=["GET"])
@swag_from(
    {
        "tags": ["books"],
        "summary": "Get books within a price range",
        "description": "Returns books filtered by minimum and maximum price.",
        "parameters": [
            {
                "name": "min_price",
                "in": "query",
                "type": "number",
                "required": False,
                "default": 0,
                "description": "Minimum price filter",
            },
            {
                "name": "max_price",
                "in": "query",
                "type": "number",
                "required": False,
                "default": 1000,
                "description": "Maximum price filter",
            },
        ],
        "responses": {
            200: {
                "description": "List of books within price range",
                "schema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "title": {"type": "string"},
                            "author": {"type": "string"},
                            "price": {"type": "number"},
                            "stars": {"type": "integer"},
                            "category_id": {"type": "integer"},
                            "category_name": {"type": "string"},
                            "url": {"type": "string"},
                            "image_url": {"type": "string"},
                        },
                    },
                },
            },
            400: {"description": "Invalid price parameters"},
            500: {"description": "Internal Server Error"},
        },
    }
)
def get_books_by_price_range():
    """
    Get books within a price range

    Returns books filtered by minimum and maximum price.
    """
    try:
        min_price = float(request.args.get("min_price", 0))
        max_price = float(request.args.get("max_price", 1000))
    except ValueError:
        return jsonify({"error": "Invalid price parameters"}), 400

    books_repository = BooksRepository(db_connection_handler)
    books = books_repository.get_books_by_price_range(min_price, max_price)

    return jsonify(books)
