import uuid

from sqlalchemy import Column, String

from src.db.base import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    name = Column(String)

    def to_dict(self):
        """Convert Category object to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "name": self.name,
        }
