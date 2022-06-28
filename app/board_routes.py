from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board


# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

def validate_key():
    request_board = request.get_json()
    if "title" not in request_board or "owner" not in request_board:
        abort(make_response({"details": "Invalid data"}, 400))
    return request_board

# helper function for validate id
def get_board_or_abort(board_id):
    try:
        board_id = int(board_id)
    except ValueError:
        abort(make_response({"message": f"The task id {board_id} is invalid. The id must be integer."}, 400))
    
    boards = Board.query.all()
    for board in boards:
        if board.id == board_id:
            return board
    abort(make_response({"message": f"The task id {board_id} is not found"}, 404))

@boards_bp.route("", methods=["POST"])
def create_board():
    request_board = validate_key()
    new_board = Board(
        title = request_board["title"],
        owner = request_board["owner"]
    )

    db.session.add(new_board)
    db.session.commit()
    return jsonify({"board": new_board.to_dict_board()}), 201


