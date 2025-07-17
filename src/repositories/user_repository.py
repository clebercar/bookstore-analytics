from sqlalchemy.exc import IntegrityError

from src.models.user import User


class UserRepository:
    def __init__(self, db_connection) -> None:
        self.__db_connection = db_connection

    def create_user(self, user: User):
        with self.__db_connection as database:
            try:
                database.session.add(user)
                database.session.commit()
            except IntegrityError:
                database.session.rollback()
                raise Exception("Email already exists")

    def get_user_by_email_and_password(self, email: str, password: str):
        with self.__db_connection as database:
            return (
                database.session.query(User)
                .filter(User.email == email)
                .filter(User.password == password)
                .first()
            )
