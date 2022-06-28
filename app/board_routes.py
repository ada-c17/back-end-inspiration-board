from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")


#get all elements 
@boards_bp.route("", methods = ["GET"])
def get_all_boards():
    boards = Board.query.all()
    return jsonify([board.to_dict_board() for board in boards]), 200
