from flask import Blueprint, request, jsonify, make_response, abort
from app import db

board_bp = Blueprint("board_bp", __name__, url_prefix="/boards")

#validation board helper function
def validate_board(board_id):
    board_id=int(board_id)
    boards = Board.query.all()
    for board in boards:
        if board_id==boards.board_id:
            return board
    abort(make_response({'details': 'This Board does not exist'}, 404))

# GET /boards

# POST /boards
