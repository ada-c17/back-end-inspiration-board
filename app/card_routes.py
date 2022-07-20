from flask import Blueprint, request, abort, make_response, jsonify
from app import db
from app.models.card import Card

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# GET 
@cards_bp.route("", methods=["GET"])
def get_cards():
    cards = Card.query.all()

    cards_response = [card.to_dict() for card in cards]

    return jsonify(cards_response), 200

def validate_card(id):
    card = Card.query.get(id)

    if not card:
        abort(make_response({"message": f"card {id} not found"}, 404))

    return card

# DELETE
@cards_bp.route("/<id>", methods=["DELETE"])
def delete_card(id):
    card = validate_card(id)

    db.session.delete(card)
    db.session.commit()

    return jsonify({"details": f'card id:{id} successfully deleted'}), 200

# PATCH /cards/card_id
    # increase likes_count
@cards_bp.route("/<id>", methods=["PATCH"])
def update_likes_count(id):
    card = validate_card(id)

    card.likes_count += 1
    db.session.commit()

    return jsonify(card.to_dict()), 200