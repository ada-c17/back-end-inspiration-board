from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from helper_function import validate_input_key_for_post_or_update

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")


@boards_bp.route("", methods=["POST"])
def create_board():
    request_board = validate_input_key_for_post_or_update()
    new_board = Board(
        title = request_board["title"],
        owner = request_board["owner"]
    )

    db.session.add(new_board)
    db.session.commit()
    return jsonify({"board": new_board.to_dict_board()}), 201


