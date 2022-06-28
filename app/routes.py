from crypt import methods
from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
# example_bp = Blueprint('example_bp', __name__)

boards_bp = Blueprint("boards", __name__, url_prefix="/boards") 

# Get board
@boards_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()
    boards_response = [board.to_dict() for board in boards]

    return jsonify(boards_response), 200

# Create board
@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()

    try:
        new_board = Board.create(request_body)
    except KeyError:
        return make_response({"details":"Invalid data"}, 400)

    db.session.add(new_board)
    db.session.commit()

    return jsonify({"board":new_board.to_dict()}), 201
    