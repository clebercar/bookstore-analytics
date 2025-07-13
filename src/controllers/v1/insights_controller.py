from collections import Counter
from statistics import mean

from flask import Blueprint, jsonify

from src.db.connection import db_connection_handler
from src.repositories.books_repository import BooksRepository
from src.repositories.categories_repository import CategoriesRepository

insights_controller = Blueprint("insights_controller", __name__)


@insights_controller.route("/api/v1/stats/overview", methods=["GET"])
def stats_overview():
    books_repository = BooksRepository(db_connection_handler)
    books = books_repository.list_books()

    if not books:
        return jsonify(
            {"total_books": 0, "average_price": 0, "ratings_distribution": {}}
        )

    # Calculate total number of books
    total_books = len(books)

    # Calculate average price
    prices = [book["price"] for book in books if book["price"] is not None]
    average_price = round(mean(prices), 2) if prices else 0

    # Calculate ratings distribution
    ratings = [book["stars"] for book in books if book["stars"] is not None]
    ratings_distribution = dict(Counter(ratings))

    # Sort ratings distribution by rating value
    ratings_distribution = dict(sorted(ratings_distribution.items()))

    return jsonify(
        {
            "total_books": total_books,
            "average_price": average_price,
            "ratings_distribution": ratings_distribution,
        }
    )


@insights_controller.route("/api/v1/stats/categories", methods=["GET"])
def stats_categories():
    books_repository = BooksRepository(db_connection_handler)
    categories_repository = CategoriesRepository(db_connection_handler)

    # Get all books with their categories
    books = books_repository.list_books()
    categories = categories_repository.list_categories()

    # Create a mapping of category_id to category name
    category_map = {category.id: category.name for category in categories}

    # Group books by category
    category_stats = {}

    for book in books:
        category_id = book["category_id"]
        category_name = category_map.get(category_id, "Unknown")

        if category_name not in category_stats:
            category_stats[category_name] = {
                "number_of_books": 0,
                "prices": [],
                "average_price": 0,
                "min_price": 0,
                "max_price": 0,
            }

        category_stats[category_name]["number_of_books"] += 1

        if book["price"] is not None:
            category_stats[category_name]["prices"].append(book["price"])

    # Calculate price statistics for each category
    for category_name, stats in category_stats.items():
        prices = stats["prices"]
        if prices:
            stats["average_price"] = round(mean(prices), 2)
            stats["min_price"] = round(min(prices), 2)
            stats["max_price"] = round(max(prices), 2)
        else:
            stats["average_price"] = 0
            stats["min_price"] = 0
            stats["max_price"] = 0

        # Remove the raw prices list as it's not needed in the response
        del stats["prices"]

    return jsonify(
        {"categories": category_stats, "total_categories": len(category_stats)}
    )
