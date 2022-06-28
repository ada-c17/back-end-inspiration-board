from flask import Blueprint, request, jsonify, make_response
from app import db
from .models.board import Board
from .models.card import Card

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")
# cards_bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

@boards_bp.route("/", methods=["GET"])
def get_boards():
    boards = Board.query.all()
    boards_response = [board.to_dict() for board in boards]

    return jsonify(boards_response)
