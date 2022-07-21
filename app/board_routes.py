from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card
from .routes_helper import success_msg, make_model, get_model_by_id

bp = Blueprint("boards_bp", __name__, url_prefix="/boards")


#GET/boards
@bp.route("", methods=("GET",))
def get_all_boards():
    boards = Board.query.order_by("board_id").all()
    board_list = [board.to_dict() for board in boards]
    return jsonify(board_list), 200


#GET/cards by board_id
@bp.route("/<board_id>/cards", methods=["GET"])
def get_all_cards(board_id):
    board = get_model_by_id(Board, board_id)
    cards = board.cards 
    card_list =  [card.to_dict() for card in cards]
    return jsonify(card_list), 200


#POST/boards
@bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    new_board = make_model(Board, request_body)
    db.session.add(new_board)
    db.session.commit()
    return jsonify({"board": new_board.to_dict()}), 201


#POST/card by board_id
@bp.route("/<board_id>/cards", methods=["POST"])
def create_card(board_id):
    request_body = request.get_json()
    new_card = make_model(Card, request_body, board_id=board_id)
    db.session.add(new_card)
    db.session.commit()
    return jsonify({"card": new_card.to_dict()}), 201


#DELETE/board by id
@bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = get_model_by_id(Board, board_id)
    db.session.delete(board)
    db.session.commit()
    return success_msg(f"Board #{board.board_id} successfully deleted",200)