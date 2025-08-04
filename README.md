# Book Recommendation API

A comprehensive Flask-based REST API for book management, analytics, and machine learning predictions. This project includes user authentication, data scraping, statistical insights, and ML-powered book rating predictions.

## 🚀 Features

-   **User Authentication**: JWT-based authentication system with user registration and login
-   **Book Management**: Complete CRUD operations for books with search functionality
-   **Data Scraping**: Automated web scraping to collect book data
-   **Analytics & Insights**: Comprehensive statistics and analytics dashboard
-   **Machine Learning**: ML model for predicting book ratings based on price and category
-   **API Documentation**: Interactive Swagger documentation
-   **Database**: SQLite with proper schema and relationships

## 📋 Prerequisites

-   Python 3.12
-   Pipenv

## 🛠️ Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd tech-challenge
    ```
2. Install dependencies:
    ```bash
    pipenv install
    ```
3. Set up environment variables:
    ```bash
    # Create a .env file with:
    SECRET_KEY=your-secret-key-here
    ```

## 🚀 Running the API

Start the development server:

```bash
pipenv run python main.py
```

Or run directly with Flask:

```bash
pipenv run flask --app main.py run --host 0.0.0.0 --port 3000 --debug
```

The API will be available at: **http://localhost:3000**

## 📚 API Documentation

Once the server is running, you can access:

-   **Interactive API Documentation**: http://localhost:3000/docs
-   **API Base URL**: http://localhost:3000

## 🔐 Authentication Endpoints

### User Registration

-   `POST /api/v1/users` - Register a new user
    -   Required fields: `name`, `email`, `password`, `confirm_password`

### Authentication

-   `POST /api/v1/auth/login` - User login (returns JWT token)
    -   Required fields: `email`, `password`
-   `POST /api/v1/auth/refresh` - Refresh JWT token
    -   Required fields: `token`

## 📖 Book Management Endpoints

### Books

-   `GET /api/v1/books` - List all books
-   `GET /api/v1/books/<id>` - Get book by ID
-   `GET /api/v1/books/search?title=<title>&category=<category>` - Search books

### Categories

-   `GET /api/v1/categories` - List all categories

## 📊 Analytics & Insights Endpoints

### Statistics

-   `GET /api/v1/stats/overview` - General collection statistics
    -   Total books, average price, ratings distribution
-   `GET /api/v1/stats/categories` - Detailed statistics by category
    -   Number of books, price statistics per category

## 🤖 Machine Learning Endpoints

### ML Features

-   `GET /api/v1/ml/features` - Get machine learning features
-   `GET /api/v1/ml/training-data` - Get training data used for model
-   `POST /api/v1/ml/predictions` - Predict book rating
    -   Required fields: `price`, `category`
    -   Returns predicted rating (1-5 stars)

## 🔄 Data Collection Endpoints

### Scraping

-   `POST /api/v1/scrapping/trigger` - Trigger data scraping process
    -   Requires JWT authentication
    -   Runs asynchronously in background

## 🏥 Health Check

-   `GET /api/v1/health` - Health check endpoint

## 🗄️ Database Schema

The application uses SQLite with the following models:

### User Model

-   `id`: Integer primary key
-   `name`: User's full name
-   `email`: Unique email address
-   `password`: Hashed password

### Book Model

-   `id`: UUID primary key
-   `title`: Book title
-   `price`: Book price
-   `availability`: Availability status
-   `stars`: Rating (integer 1-5)
-   `image_url`: Book cover image URL
-   `category_id`: Foreign key to Category

### Category Model

-   `id`: UUID primary key
-   `name`: Category name

## 🏗️ Project Structure

```
tech-challenge/
├── src/
│   ├── controllers/          # API route handlers
│   │   └── v1/
│   │       ├── auth_controller.py          # Authentication endpoints
│   │       ├── books_controller.py         # Book management
│   │       ├── health_controller.py        # Health checks
│   │       ├── insights_controller.py      # Analytics & statistics
│   │       ├── machine_learning_controller.py  # ML predictions
│   │       ├── scrapping_controller.py     # Data collection
│   │       └── user_controller.py          # User management
│   ├── db/
│   │   ├── base.py           # Database base configuration
│   │   ├── connection.py     # Database connection handler
│   │   └── schema.sql        # Database schema
│   ├── interfaces/           # Repository interfaces
│   │   ├── books_repository_interface.py
│   │   └── categories_repository_interface.py
│   ├── ml/                   # Machine Learning components
│   │   ├── model.joblib      # Trained ML model
│   │   ├── category_encoder.joblib  # Category encoder
│   │   ├── model_training.py # Model training script
│   │   └── predict_service.py # Prediction service
│   ├── models/               # Data models
│   │   ├── book.py           # Book model
│   │   ├── category.py       # Category model
│   │   └── user.py           # User model
│   ├── repositories/         # Data access layer
│   │   ├── books_repository.py
│   │   ├── categories_repository.py
│   │   └── user_repository.py
│   ├── scripts/
│   │   └── scrapper.py       # Web scraping utilities
│   └── server.py             # Flask application setup
├── main.py                   # Application entry point
├── Pipfile                   # Python dependencies
├── Pipfile.lock              # Locked dependencies
├── storage.db                # SQLite database
├── FIAP - FASE 1.postman_collection.json  # Postman collection
├── app_architecture_diagram.html  # Application architecture diagram
└── README.md                 # This file
```

### 📐 Architecture Diagram

For a visual representation of the application's architecture, see: [app_architecture_diagram.html](https://bookstore-analytics.onrender.com/diagram)

## 🔧 Development

The server runs with debug mode enabled, so any changes to the code will automatically restart the server.

### Key Features Implemented:

1. **Authentication System**: Complete JWT-based authentication with user registration and login
2. **Machine Learning**: Trained model for predicting book ratings based on price and category
3. **Data Scraping**: Automated collection of book data from web sources
4. **Analytics Dashboard**: Comprehensive statistics and insights
5. **API Documentation**: Interactive Swagger documentation
6. **Database Management**: Proper SQLite schema with relationships
7. **Error Handling**: Comprehensive error handling and validation

## 📝 API Usage Examples

### Register a new user:

```bash
curl -X POST http://localhost:3000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123",
    "confirm_password": "password123"
  }'
```

### Login:

```bash
curl -X POST http://localhost:3000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

### Predict book rating:

```bash
curl -X POST http://localhost:3000/api/v1/ml/predictions \
  -H "Content-Type: application/json" \
  -d '{
    "price": 29.99,
    "category": "Fiction"
  }'
```

### Get analytics:

```bash
curl http://localhost:3000/api/v1/stats/overview
```

### Get categories:

```bash
curl http://localhost:3000/api/v1/categories
```

## 🎯 Machine Learning Model

The ML model predicts book ratings (1-5 stars) based on:

-   **Price**: Book price in currency units
-   **Category**: Book category (encoded)

The model is trained on historical book data and provides predictions through the `/api/v1/ml/predictions` endpoint.

## 📊 Analytics Features

The API provides comprehensive analytics including:

-   Total book count and average prices
-   Rating distribution analysis
-   Category-wise statistics
-   Price range analysis per category

## 🔒 Security Features

-   JWT token-based authentication
-   Password hashing for user security
-   Input validation and sanitization
-   Protected endpoints requiring authentication
-   Token expiration and refresh mechanisms

This project demonstrates a complete full-stack application with modern web development practices, machine learning integration, and comprehensive API design.
