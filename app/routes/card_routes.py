from flask import Blueprint, request, jsonify
from app import db
from app.models.card import Card
from app.models.board import Board
from app.helper import get_card_or_abort, get_board_or_abort, validate_card
from app.routes.board_routes import boards_bp

cards_bp = Blueprint('cards_bp', __name__, url_prefix="/cards")


# POST /boards/<board_id>/cards
# CREATE A CARD
@boards_bp.route('/<board_id>/cards', methods=['POST'])
def add_cards_to_boards(board_id):
    request_body = request.get_json()
    new_card = validate_card(request_body, board_id)

    # add record to the table
    db.session.add(new_card)
    db.session.commit()

    return jsonify(new_card.to_dict()), 201


# @boards_bp.route('/<board_id>/cards', methods=['POST'])
# def add_cards_to_boards(board_id):

#     board = get_board_or_abort(board_id)
#     request_body = request.get_json()

#     try:
#         card_ids = request_body["card_ids"]
#     except KeyError:
#         return { "details": "Invalid data, missing card_ids"}, 400
#     if not isinstance(card_ids,list):
#         return { "details": "Expected list of card ids"}, 400
    
#     cards = []
#     for id in card_ids:
#         card = get_card_or_abort(id)
#         cards.append(card)

#     for card in cards:
#         card.board_id=board_id

#     db.session.commit()

#     return jsonify(
#         {
#             "id": board.board_id,
#             "card_ids": card_ids
#         }
#     ),200

# GET /boards/<board_id>/cards
@boards_bp.route('/<board_id>/cards', methods=['GET'])
def get_cards_at_one_board(board_id):
    board = get_board_or_abort(board_id)
    cards = []
    for card in board.cards:
        cards.append(card.to_dict())
    return ({
                "board_id": board.board_id,
                "title": board.title,
                "owner": board.owner,
                "cards": cards
            }), 200


# GET one card
@boards_bp.route('/<board_id>/cards/<card_id>', methods=['GET'])
def get_one_card_at_one_board(board_id, card_id):
    card = get_card_or_abort(card_id)

    return jsonify(card.to_dict()), 200




# DELETE /boards/<board_id>/cards
@cards_bp.route('/<card_id>', methods=['DELETE'])
def delete_one_card(card_id):
    card = get_card_or_abort(card_id)
    db.session.delete(card)
    db.session.commit()

    return {
        "details" : f'Card {card.card_id} {card.message} successfully deleted'
    }, 200

# PATCH /cards/<card_id>/like ???
@cards_bp.route('/<card_id>/like', methods=['PATCH'])
def update_card(card_id):
    card = get_card_or_abort(card_id)
    # request_body = request.get_json()
    
    # try:
    #     card.likes_count = request_body["likes_count"]
    #     # card.likes_count = request_body.get("likes_count")
    
    # except KeyError:
    #     return {
    #         "msg" : "Message and likes are required" 
    #     }, 400
    card.likes_count += 1
    db.session.commit()
    return jsonify(card.to_dict()), 200