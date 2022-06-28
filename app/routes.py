from flask import Blueprint, request, jsonify, make_response
from flask import abort  # added for validations
from app import db
# import models:
from .models.board import Board

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint("board_bp", __name__, url_prefix="/boards")

# Board Model routes:

# 1. POST - Create a new board, by filling out a form. The form includes "title" and "owner" name of the board.
# POST displays ERROR msg if empty/blank/invalid/missing "title" or "owner" input.


@board_bp.route("", methods=["POST"])
def create_one_board():
    request_body = request.get_json()
    try:
        # need to add validating here
        new_board = Board(
            title=request_body['title'], owner=request_body['owner'])
    except:
        abort(make_response(
            {"details": "Invalid data. Title or owner missing or invalid from board"}, 400))
    db.session.add(new_board)
    db.session.commit()
    return {
        'id': new_board.id,
        'msg': f'New board {new_board.title} created'
    }, 201

# 2.GET- Read; View a list of all boards
# 3. GET - Read; Select a specific board

# Helper function to validate board_id:


def validate_board(board_id):
    try:
        board_id = int(board_id)
    except:
        abort(make_response(
            {"message": f"Planet: {board_id} is not a valid planet id"}, 400))
    board = Board.query.get(board_id)
    if not board:
        abort(make_response(
            {"message": f"Planet: #{board_id} not found"}, 404))
    return board
