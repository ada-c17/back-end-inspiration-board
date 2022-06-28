from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card


##### TABLE OF CONTENTS #############################################

#   [0] IMPORTS
#   [1] BLUEPRINT DEFINITIONS
#   [2] BOARD ENDPOINTS
#   [3] CARD ENDPOINTS


##### [1] BLUEPRINT DEFINITIONS #####################################

board_bp = Blueprint('board_bp', __name__, url_prefix='/boards')
card_bp = Blueprint('card_bp', __name__, url_prefix='/cards')


##### [2] BOARD ENDPOINTS ###########################################

@board_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()

    response = []
    for board in boards:
        response.append(board.to_dict())
    
    return jsonify(response), 200


@board_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    chosen_board = Board.query.get(board_id)
    return jsonify(chosen_board.to_dict()), 200


@board_bp.route("", methods=["POST"])
def post_board():
    request_body = request.get_json()

    if "title" in request_body and "owner" in request_body:
        new_board = Board(title=request_body["title"],
                    owner=request_body["owner"])
    else:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_board)
    db.session.commit()

    return make_response({"board": new_board.to_dict()}, 201)



##### [3] CARD ENDPOINTS ############################################

def get_all_cards():
    cards = Card.query.all()
    response = []
    for card in cards:
        response.append(card.to_dict())
    return jsonify(response), 200


@card_bp.route("/<card_id>", methods=["GET"])
def get_one_card(card_id):
    chosen_card = Card.query.get(card_id)
    return jsonify(chosen_card.to_dict()), 200


@card_bp.route("", methods=["POST"])
def post_card():
    request_body = request.get_json()

    if "message" in request_body:
        if len(request_body["message"]) > 40:
            abort(make_response({"details": "Messages cannot be longer than 40 characters"}, 400))
        new_card = Card(message=request_body["message"],
                    likes_count=0)
    else:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_card)
    db.session.commit()

    return make_response({"card": new_card.to_dict()}, 201)

@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_one_card(card_id):
    chosen_card = Card.query.get(card_id)
    db.session.delete(chosen_card)
    db.session.commit()
    return {
        "message" : f'Card {card_id} successfully deleted'
    }


