from flask import Blueprint, request, jsonify, make_response
from app.models.board import Board
from app import db

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

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