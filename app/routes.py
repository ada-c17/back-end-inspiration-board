import re
from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from app.models.board import Board
import requests

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint("board_bp", __name__, url_prefix = "/boards")

@board_bp.route("", methods = ["GET"])
def get_all_boards():
    boards = Board.query.all()
    board_response = []
    for board in boards:
        board_response.append({
            "id": board.board_id,
            "title": board.title,
            "owner": board.owner,
        })
    return jsonify(board_response), 200

@board_bp.route("", methods=["POST"])
def create_one_board():
    request_body = request.get_json()
    try:
        new_board = Board(title = request_body["title"], owner = request_body["owner"])
    except KeyError:
        return {"msg":"Invalid input"}, 400
        # abort(make_response(jsonify(response), 400))
    db.session.add(new_board)
    db.session.commit()
    response = {"board":{"title":new_board.title, "owner": new_board.owner}}
    return jsonify(response), 201