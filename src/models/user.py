import uuid

from sqlalchemy import Column, String

from src.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    name = Column(String)
    email = Column(String)
    password = Column(String)
