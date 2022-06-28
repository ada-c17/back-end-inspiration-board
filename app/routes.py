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

@boards_bp.route('/', methods=['POST'])
def create_board():
    request_body = request.get_json()

    if not "title" in request_body or not "owner" in request_body:  # or \
        # not "completed_at" in request_body:
        return jsonify({
            "details": "Invalid data"
        }), 400

    new_board = Board(title=request_body["title"],
                    owner=request_body["owner"]
                    )

    db.session.add(new_board)
    db.session.commit()

    return {
        "board": new_board.to_dict()
    }, 201

@boards_bp.route("/<board_id>", methods=["GET"])
def get_board_by_id(board_id):
    board = Board.query.get(board_id)

    if board:
        return {"board": board.to_dict()}
    
    else:
        return jsonify({
            "details": f"ID {board_id} does not exist"
        }), 404