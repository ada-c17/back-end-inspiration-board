from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config={'TESTING': False}):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        os.environ.get("SQLALCHEMY_DATABASE_URI") if not test_config['TESTING'] 
        else os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")
        )


    from app.models.card import Card
    from app.models.board import Board
    
    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import boards_bp, cards_bp
    app.register_blueprint(cards_bp)
    app.register_blueprint(boards_bp)


    CORS(app)
    return app
