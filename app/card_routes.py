from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from app.models.board import Board
from .routes_helper import get_record_by_id, make_record_safely

# example_bp = Blueprint('example_bp', __name__)
card_bp = Blueprint('card_bp', __name__, url_prefix="/boards/")

# create new card to board by id
@card_bp.route("<board_id>/cards", methods=["POST"], strict_slashes=False)
def create_card(board_id):
    get_record_by_id(Board,board_id)
    
    request_body = request.get_json()
    new_card = make_record_safely(Card, request_body )

    db.session.add(new_card)
    db.session.commit()

    return make_response("Success", 201)

# delete single card
@card_bp.route("<board_id>/cards/<card_id>", methods=["DELETE"], strict_slashes=False)
def delete_card(board_id, card_id):
    get_record_by_id(Board,board_id)
    card = get_record_by_id(Card,card_id)
    
    card = Card.query.get(card_id)

    db.session.delete(card)
    db.session.commit()
    return make_response("Card successfully deleted", 200)

# add one like
@card_bp.route("<board_id>/cards/<card_id>/like", methods=["PATCH"], strict_slashes=False)
def add_like(card_id):
    # validate stuff
    card = Card.query.get(card_id)
    card.likes_count += 1

    db.session.commit()
    return make_response("Success", 200)



# OPTIONAL ENHANCEMENT
# update one card 
# @card_bp.route("<board_id>/cards/<card_id>", methods=["PATCH"], strict_slashes=False)
# def update_card(board_id, card_id):
#     #validate board_id
#     #validate card_id -- validate that card id is a valid ID
#     # and that it is assigned to the board
#     card = Card.query.get(card_id)

#     request_body = request.get_json()
#     card.message = request_body["message"]

#     db.session.commit()
#     return make_response("Success", 200)

# #get all cards for all boards
# @card_bp.route("/cards", methods=["GET"], strict_slashes=False)
# def get_cards():
#     cards = Card.query.all()
#     cards_response = [card.to_json() for card in cards]
#     return jsonify(cards_response)