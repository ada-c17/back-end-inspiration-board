from flask import Flask
import flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

def creare_app(test_conf=None):
    app = Flask(_name_)  
    from app.models.board import Board
    return app