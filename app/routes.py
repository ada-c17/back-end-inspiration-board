import re
from socket import J1939_PGN_ADDRESS_COMMANDED
from attr import validate
from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
from app.models.board import Board
import requests

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint("board_bp", __name__, url_prefix = "/boards")

def validate_board(board_id):
    try:
        board = int(board_id)
    except ValueError:
        response = {"msg":f"Invalid id: {board_id}"}
        abort(make_response(jsonify(response), 400))
    chosen_board = Board.query.get(board_id)

    if chosen_board is None:
        response = {"msg":f"Could not find board with id #{board_id}"}
        abort(make_response(jsonify(response), 400))
    return chosen_board


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

@board_bp.route("/<board_id>", methods = ["GET"])
def get_one_board(board_id):
    chosen_board = validate_board(board_id)
    response = {"board":{
        "id": chosen_board.board_id,
        "title": chosen_board.title,
        "owner": chosen_board.owner,
    }}
    return jsonify(response), 200

@board_bp.route("/<board_id>/cards", methods = ["GET"])
def get_cards_from_one_board(board_id):
    chosen_board = validate_board(board_id)
    response = {
        "id": chosen_board.board_id,
        "title": chosen_board.title,
        "cards":[]
    }
    for card in chosen_board.cards:
        response["cards"].append({
            "id":card.card_id,
            "board_id":chosen_board.board_id,
            "title": card.title,
            "owner": card.owner,
        })
    return jsonify(response), 200
