from abc import ABC, abstractmethod


class CategoriesRepositoryInterface(ABC):
    @abstractmethod
    def list_categories(self):
        pass

    @abstractmethod
    def category_exists_by_name(self, name: str) -> bool:
        pass

    @abstractmethod
    def save_category(self, name: str) -> str:
        pass

    @abstractmethod
    def get_category_by_name(self, name: str):
        pass
