from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if not test_config:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    from app.models.board import Board
    from app.models.card import Card

    db.init_app(app)
    migrate.init_app(app, db)


    from app.routes.card_routes import cards_bp
    app.register_blueprint(cards_bp)

    from app.routes.board_routes import boards_bp
    app.register_blueprint(boards_bp)

    CORS(app)
    return app
