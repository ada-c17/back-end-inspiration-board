from flask import Blueprint, request, jsonify, make_response
from app import db


cards_bp = Blueprint('cards', __name__, url_prefix="/cards")




#DELETE a card
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_one_card(card_id):
    pass

#UPDATE likes "+1" for a card
@cards_bp.route("/<card_id>", methods=["PUT"])
def update_likes_for_one_card(card_id):
    pass