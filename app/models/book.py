import uuid
from sqlalchemy import Column, Integer, String, Float
from app.db.database import Base 

class Book(Base):
  __tablename__ = "books"

  id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
  title = Column(String)
  price = Column(Float)
  availability = Column(String)
  stars = Column(Integer)
  image_url = Column(String)
  category = Column(String)