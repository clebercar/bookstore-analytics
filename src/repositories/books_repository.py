from typing import Optional

from sqlalchemy.exc import NoResultFound

from src.interfaces.books_repository_interface import BooksRepositoryInterface
from src.models.book import Book
from src.models.category import Category


class BooksRepository(BooksRepositoryInterface):
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection

    def save_books(self, books: list[Book]):
        with self.__db_connection as database:
            database.session.add_all(books)
            database.session.commit()

    def get_book_by_id(self, book_id: int) -> Optional[dict]:
        with self.__db_connection as database:
            try:
                book = database.session.query(Book).filter(Book.id == book_id).one()
                return book.to_dict()
            except NoResultFound:
                return None

    def list_books(
        self, title: Optional[str] = None, category: Optional[str] = None
    ) -> list[dict]:
        with self.__db_connection as database:
            query = database.session.query(Book).join(
                Category, Book.category_id == Category.id
            )

            if title:
                query = query.filter(Book.title.ilike(f"%{title}%"))

            if category:
                query = query.filter(Category.name.ilike(f"%{category}%"))

            books = query.all()
            return [book.to_dict() for book in books]

    def top_rated_books(self) -> list[dict]:
        with self.__db_connection as database:
            books = (
                database.session.query(Book).order_by(Book.stars.desc()).limit(10).all()
            )
            return [book.to_dict() for book in books]

    def get_books_by_price_range(
        self, min_price: float, max_price: float
    ) -> list[dict]:
        with self.__db_connection as database:
            books = (
                database.session.query(Book)
                .filter(Book.price >= min_price)
                .filter(Book.price <= max_price)
                .all()
            )
            return [book.to_dict() for book in books]
