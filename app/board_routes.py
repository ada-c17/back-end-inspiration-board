from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

# helper function for validate key of input
def validate_input_key_for_post_or_update():
    request_board = request.get_json()
    if "title" not in request_board or "owner" not in request_board:
        abort(make_response({"details": "Invalid data"}, 400))
    return request_board



