from src.interfaces.categories_repository_interface import CategoriesRepositoryInterface
from src.models.category import Category


class CategoriesRepository(CategoriesRepositoryInterface):
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection

    def list_categories(self):
        with self.__db_connection as database:
            categories = database.session.query(Category).all()
            return [category.to_dict() for category in categories]

    def category_exists_by_name(self, name: str) -> bool:
        with self.__db_connection as database:
            category = (
                database.session.query(Category).filter(Category.name == name).first()
            )

            return category is not None

    def save_category(self, name: str):
        with self.__db_connection as database:
            category = Category(name=name)
            database.session.add(category)
            database.session.commit()

            return category.id

    def get_category_by_name(self, name: str):
        with self.__db_connection as database:
            return (
                database.session.query(Category).filter(Category.name == name).first()
            )
