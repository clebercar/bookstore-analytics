# Books Store API

A Flask-based REST API for managing books with SQLite database.

## Prerequisites

-   Python 3.12
-   Pipenv

## Installation

1. Clone the repository
2. Install dependencies:

```bash
pipenv install
```

## Running the API

Start the development server:

```bash
pipenv run python main.py
```

Or run directly with Flask:

```bash
pipenv run flask --app main.py run --host 0.0.0.0 --port 3000 --debug
```

## API Documentation

Once the server is running, you can access:

-   **API Base URL**: http://localhost:3000

### Available Endpoints

#### Books

-   `GET /api/v1/books` - List all books
-   `GET /api/v1/books/<id>` - Get book by ID
-   `GET /api/v1/books/search?title=<title>&category=<category>` - Search books

#### Health

-   `GET /api/v1/health` - Health check endpoint

#### Statistics

-   `GET /api/v1/stats/overview` - General collection statistics (total books, average price, ratings distribution)
-   `GET /api/v1/stats/categories` - Detailed statistics by category (number of books, prices per category)

## Project Structure

```
tech-challenge/
├── src/
│   ├── controllers/     # API route handlers
│   │   └── v1/
│   │       ├── books_controller.py
│   │       ├── health_controller.py
│   │       └── insights_controller.py
│   ├── db/
│   │   ├── base.py      # Database base configuration
│   │   ├── connection.py # Database connection handler
│   │   └── schema.sql   # Database schema
│   ├── interfaces/       # Repository interfaces
│   ├── models/          # Data models
│   │   ├── book.py      # Book model
│   │   └── category.py  # Category model
│   ├── repositories/    # Data access layer
│   │   ├── books_repository.py
│   │   └── categories_repository.py
│   ├── scripts/
│   │   └── scrapper.py  # Web scraping utilities
│   └── server.py        # Flask application setup
├── main.py              # Application entry point
├── Pipfile              # Python dependencies
└── README.md           # This file
```

## Database

The application uses SQLite with the following models:

### Book Model

-   `id`: UUID primary key
-   `title`: Book title
-   `price`: Book price
-   `availability`: Availability status
-   `stars`: Rating (integer)
-   `image_url`: Book cover image URL
-   `category_id`: Foreign key to Category

### Category Model

-   `id`: UUID primary key
-   `name`: Category name

## Development

The server runs with debug mode enabled, so any changes to the code will automatically restart the server.
