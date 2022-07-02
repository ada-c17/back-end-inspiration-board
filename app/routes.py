from flask import Blueprint, request, jsonify, make_response
from .models.board import Board
from .models.card import Card
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

@board_bp.route("/<board_id>/cards", methods=("POST",))
def post_one_card_to_board(board_id):
    request_body = request.get_json()

    board = validate_model(Board, board_id)

    try:
        input_message = request_body["message"]
        if len(input_message) <= 40:
            new_card = Card(message=input_message, board_id=board_id)
        else:
            error_message("message is greater than 40 characters", 400)
    except KeyError as err:
        error_message(f"missing required {err}", 400)

    db.session.add(new_card)
    db.session.commit()

    return jsonify(new_card.to_dict()), 201

@board_bp.route("/<board_id>/cards", methods=("GET",))
def get_cards_of_board(board_id):
    board = validate_model(Board, board_id)
    cards_dict = [card.to_dict() for card in board.cards]

    result = board.to_dict()
    result["cards"] = cards_dict

    return jsonify(result), 200

@board_bp.route("/<board_id>/cards/<card_id>", methods=("DELETE",))
def delete_one_card_of_board(board_id, card_id):
    board = validate_model(Board, board_id)
    card = validate_model(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    return make_response(jsonify(dict(details=f'Card #{card.card_id} "{card.message}" successfully deleted'))), 200
