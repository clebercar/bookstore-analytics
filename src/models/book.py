import uuid

from sqlalchemy import Column, Float, ForeignKey, Integer, String

from src.db.base import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(
        String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4())
    )
    title = Column(String)
    price = Column(Float)
    availability = Column(String)
    stars = Column(Integer)
    image_url = Column(String)
    category_id = Column(String(36), ForeignKey("categories.id"))

    def to_dict(self):
        """Convert Book object to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "availability": self.availability,
            "stars": self.stars,
            "image_url": self.image_url,
            "category_id": self.category_id,
        }

    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title}, price={self.price}, availability={self.availability}, stars={self.stars}, image_url={self.image_url}, category_id={self.category_id})>"
