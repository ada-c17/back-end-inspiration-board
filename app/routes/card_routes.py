from flask import Blueprint, request, jsonify, make_response
from app import db


cards_bp = Blueprint('cards', __name__, url_prefix="/cards")


#CREATE a new card for the selected board 
@cards_bp.route("/<board_id>", method=["POST"])
def create_new_card(board_id):
    pass

#DELETE a card
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_one_card(card_id):
    pass

#UPDATE likes "+1" for a card
@cards_bp.route("/<card_id>", method=["PUT"])
def update_likes_for_one_card(card_id):
    pass