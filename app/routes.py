from flask import Blueprint, request, jsonify, make_response, abort
from app.models.board import Board
from app import db

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")


# helper function to validate board
def validate_board(board_id):
    try:
        board_id = int(board_id)
    except:
        abort(make_response({"message":f"Board ID {board_id} is invalid"}, 400))

    board = Board.query.get(board_id)

    if not board:
        abort(make_response({"message":f"Board ID {board_id} not found"}, 404))

    return board

# routes
@boards_bp.route("", methods = ["POST"])
def create_board():
    request_body = request.get_json()

    if "title" not in request_body or "owner" not in request_body:
        return {"details": "Invalid data"}, 400

    new_board = Board(title=request_body["title"], owner=request_body["owner"])
    db.session.add(new_board)
    db.session.commit()

    return make_response({"board":new_board.to_json()}, 201)

@boards_bp.route("", methods = ["GET"])
def get_all_boards():
    boards = Board.query.all()

    boards_response = []
    for board in boards:
        boards_response.append(board.to_json())
    
    return jsonify(boards_response)

@boards_bp.route("/<board_id>", methods = ["GET"])
def get_one_board(board_id):
    board = validate_board(board_id)

    return make_response({"board":board.to_json()}, 200)

    