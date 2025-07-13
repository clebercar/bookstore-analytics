# Books Store API

A FastAPI-based REST API for managing books with SQLite database.

## Prerequisites

- Python 3.12
- Pipenv

## Installation

1. Clone the repository
2. Install dependencies:

```bash
pipenv install
```

## Running the API

Start the development server:

```bash
pipenv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Base URL**: http://localhost:8000

## Project Structure

```
tech-challenge/
├── app/
│   ├── controllers/     # API route handlers
│   ├── db/
│   │   └── database.py  # Database configuration
│   ├── models/
│   │   └── book.py      # Book model
│   ├── scripts/
│   │   └── scrapper.py  # Web scraping utilities
│   └── main.py          # FastAPI application entry point
├── Pipfile              # Python dependencies
└── README.md           # This file
```

## Database

The application uses SQLite with the following Book model:

- `id`: UUID primary key
- `title`: Book title
- `price`: Book price
- `availability`: Availability status
- `stars`: Rating (integer)
- `image_url`: Book cover image URL
- `category`: Book category

## Development

The server runs with hot reload enabled, so any changes to the code will automatically restart the server.
