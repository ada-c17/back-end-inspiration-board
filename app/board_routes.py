from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint('board_bp', __name__, url_prefix="/boards")

@board_bp.route("/<board_id>", strict_slashes=False)
def get_one_board(board_id):
    #validate board_id
    board = Board.query.get(board_id)
    return {
            "title": board.title,
            "owner": board.owner,
            "cards": [card.to_dict() for card in board.cards]
            }