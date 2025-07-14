from flask import Flask
from flask_cors import CORS

from src.controllers.v1.books_controller import books_controller
from src.controllers.v1.health_controller import health_controller
from src.controllers.v1.insights_controller import insights_controller
from src.controllers.v1.machine_learning_controller import machine_learning_controller
from src.db.connection import db_connection_handler

db_connection_handler.connect_to_db()

app = Flask(__name__)
CORS(app)

app.register_blueprint(books_controller)
app.register_blueprint(health_controller)
app.register_blueprint(insights_controller)
app.register_blueprint(machine_learning_controller)
