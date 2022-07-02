from flask import Blueprint, request, jsonify, make_response
from .models.board import Board
from .routes_helper_functions import *
from app import db

board_bp = Blueprint("boards", __name__, url_prefix="/boards")

@board_bp.route("", methods=("POST",))
def post_one_board():
    request_body = request.get_json()

    try:
        new_board = Board(title=request_body["title"], owner=request_body["owner"])
    except KeyError as err:
        error_message(f"missing required {err}", 400)

    db.session.add(new_board)
    db.session.commit()

    return jsonify(new_board.to_dict()), 201

@board_bp.route("", methods=("GET",))
def get_boards():

    boards = Board.query.all()

    result_list = [board.to_dict() for board in boards]

    return jsonify(result_list), 200

@board_bp.route("/<board_id>", methods=("GET",))
def get_one_board(board_id):
    board = validate_model(Board, board_id)

    return jsonify(board.to_dict()), 200
