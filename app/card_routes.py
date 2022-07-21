from flask import Blueprint, jsonify
from .models.card import Card
from .routes_helper_functions import *
from app import db

card_bp = Blueprint("cards", __name__, url_prefix="/cards")

@card_bp.route("/<card_id>", methods=("DELETE",))
def delete_one_card_of_board(card_id):
    card = validate_model(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    return make_response(jsonify(dict(details=f'Card #{card.card_id} "{card.message}" successfully deleted'))), 200

@card_bp.route('/<card_id>/like', methods=('PATCH',))
def patch_like_of_one_card(card_id):
    card = validate_model(Card, card_id)

    card.likes_count += 1

    db.session.commit()

    return make_response(jsonify(dict(details=f'Likes updated for Card #{card.card_id} to {card.likes_count}'))), 200
