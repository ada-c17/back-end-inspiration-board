from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
# from .helpers import validate_model_instance

# example_bp = Blueprint('example_bp', __name__)

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

#CREATE BOARDS
@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()

    new_board = Board.from_json(request_body)

    db.session.add(new_board)
    db.session.commit()

    return jsonify({"board": new_board.to_json()}), 201

#GET all boards
@boards_bp.route("", methods=["GET"])
def read_board():
    Boards = Board.query.all()

    boards_response = [board.to_json() for board in Boards]
        
    return jsonify(boards_response), 200
