from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from .routes_helper import get_record_by_id, make_record_safely

board_bp = Blueprint('board_bp', __name__, url_prefix="/boards/")

# Get one board and associated cards
@board_bp.route("<board_id>", methods=["GET"], strict_slashes=False)
def get_one_board(board_id):
    board = get_record_by_id(Board,board_id)
    return board.to_json()

# Create board
@board_bp.route("", methods=["POST"], strict_slashes=False)
def create_board():
    request_body = request.get_json()
    new_board = make_record_safely(Board, request_body)

    db.session.add(new_board)
    db.session.commit()

    return make_response("Success", 201)


# Get all boards
@board_bp.route("", methods=["GET"], strict_slashes=False)
def get_boards():
    boards = Board.query.all()
    boards_response = [board.to_json() for board in boards]
    return jsonify(boards_response)

