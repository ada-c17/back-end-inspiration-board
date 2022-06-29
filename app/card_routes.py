from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
from app.models.board import Board 


cards_bp = Blueprint("cards", __name__, url_prefix="/cards")


