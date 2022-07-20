from flask import Blueprint, jsonify, make_response, abort
from app.models.card import Card
from app.models.board import Board


# Helper functions
def get_card_or_abort(card_id):
    try:
        card_id = int(card_id)
    except ValueError:
        rsp = {"msg":f"Invalid id {card_id}"}
        abort(make_response(jsonify(rsp), 400))
    
    card = Card.query.get(card_id)
    if card is None:
        rsp = {"msg":f"Could not find card with id {card_id}"}
        abort(make_response(jsonify(rsp), 404))

    return card


def get_board_or_abort(board_id):
    try:
        board_id = int(board_id)
    except ValueError:
        rsp = {"msg":f"Invalid id {board_id}"}
        abort(make_response(jsonify(rsp), 400))
    
    board = Board.query.get(board_id)
    if board is None:
        rsp = {"msg":f"Could not find board with id {board_id}"}
        abort(make_response(jsonify(rsp), 404))

    return board


# Validate card has a short msg
def validate_card(request_body, board_id):
    get_board_or_abort(board_id)
    
    if "message" not in request_body:
        rsp = {
            "details": "Please enter a message. "
        }
        abort(make_response(jsonify(rsp), 400))
    elif len(request_body["message"]) > 40: 
        rsp = {
            "details": "Please enter a message shorter than 40 characters. "
        }
        abort(make_response(jsonify(rsp), 400))
    
    message = request_body["message"]

    if message and len(message) <= 40:
        new_card = Card(message=message, likes_count=0, board_id=board_id)
        return new_card
    