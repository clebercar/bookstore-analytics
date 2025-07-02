from fastapi import FastAPI
from app.models.book import Book
from app.db.database import engine

app = FastAPI(title="Books Store API")

Book.metadata.create_all(bind=engine)
