from abc import ABC, abstractmethod
from typing import Optional


class BooksRepositoryInterface(ABC):
    @abstractmethod
    def list_books(self, title: Optional[str] = None, category: Optional[str] = None):
        pass

    @abstractmethod
    def get_book_by_id(self, book_id: int):
        pass

    @abstractmethod
    def top_rated_books(self):
        pass

    @abstractmethod
    def get_books_by_price_range(self, min_price: float, max_price: float):
        pass

    @abstractmethod
    def delete_all_books(self):
        pass
