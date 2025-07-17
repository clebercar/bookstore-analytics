import os

from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask
from flask_cors import CORS

from src.controllers.v1.auth_controller import auth_controller
from src.controllers.v1.books_controller import books_controller
from src.controllers.v1.health_controller import health_controller
from src.controllers.v1.insights_controller import insights_controller
from src.controllers.v1.machine_learning_controller import machine_learning_controller
from src.controllers.v1.scrapping_controller import scrapping_controller
from src.controllers.v1.user_controller import user_controller
from src.db.connection import db_connection_handler

load_dotenv()

db_connection_handler.connect_to_db()
app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

CORS(app)

# Configure Swagger documentation
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "swagger",
            "route": "/swagger.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs",
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Book Recommendation API",
        "description": "A comprehensive API for book management, insights, and machine learning predictions",
        "version": "1.0.0",
        "contact": {"name": "API Support", "email": "support@example.com"},
    },
    "host": "localhost:3000",
    "basePath": "/",
    "schemes": ["http"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "tags": [
        {"name": "health", "description": "Health check operations"},
        {"name": "books", "description": "Book management operations"},
        {"name": "insights", "description": "Analytics and insights operations"},
        {"name": "ml", "description": "Machine learning operations"},
    ],
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

app.register_blueprint(user_controller)
app.register_blueprint(auth_controller)
app.register_blueprint(books_controller)
app.register_blueprint(health_controller)
app.register_blueprint(insights_controller)
app.register_blueprint(scrapping_controller)
app.register_blueprint(machine_learning_controller)
