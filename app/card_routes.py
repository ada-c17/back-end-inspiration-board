from flask import Blueprint, abort, request, jsonify, make_response
from app import db
from app.models.card import Card

card_bp = Blueprint("card_bp", __name__, url_prefix="/cards")


def validate_card(card_id):
    try:
        card_id = int(card_id)
    except:
        abort(make_response({"message": f"card {card_id} invalid"}, 400))

    card = Card.query.get(card_id)

    if not card:
        abort(make_response({"message": f"card {card_id} not found"}, 404))

    return card


# GET /boards/<board_id>/cards

# POST /boards/<board_id>/cards

# DELETE /cards/<card_id>

# PUT /cards/<card_id>/like
