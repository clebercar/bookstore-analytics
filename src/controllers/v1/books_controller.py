from flask import Blueprint, jsonify, request

from src.db.connection import db_connection_handler
from src.repositories.books_repository import BooksRepository

books_controller = Blueprint("books_controller", __name__)


@books_controller.route("/api/v1/books", methods=["GET"])
def list_books():
    title = request.args.get("title")
    category = request.args.get("category")

    books_repository = BooksRepository(db_connection_handler)
    books = books_repository.list_books(title=title, category=category)

    return jsonify(books)


@books_controller.route("/api/v1/books/<string:book_id>", methods=["GET"])
def get_book_by_id(book_id):
    books_repository = BooksRepository(db_connection_handler)
    book = books_repository.get_book_by_id(book_id)

    return jsonify(book)


@books_controller.route("/api/v1/books/top-rated", methods=["GET"])
def top_rated_books():
    books_repository = BooksRepository(db_connection_handler)
    books = books_repository.top_rated_books()

    return jsonify(books)


@books_controller.route("/api/v1/books/price-range", methods=["GET"])
def get_books_by_price_range():
    min_price = float(request.args.get("min_price", 0))
    max_price = float(request.args.get("max_price", 1000))

    books_repository = BooksRepository(db_connection_handler)
    books = books_repository.get_books_by_price_range(min_price, max_price)

    return jsonify(books)
