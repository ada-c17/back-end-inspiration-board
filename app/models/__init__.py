from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)
    # ... app is configured with SQLAlchemy settings
    # ... db and migrate are initialized with app

    from app.models.board import Board
    from app.models.card import Card

    return app