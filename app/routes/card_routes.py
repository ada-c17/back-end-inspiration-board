from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from .helpers import validate_model_instance

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")


# DELETE /cards/<card_id>
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_model_instance(Card, card_id, "card")
    db.session.delete(card)
    db.session.commit()

    return jsonify({"details":f'Card {card_id} "{card.message}" successfully deleted'} ), 200

# PUT /cards/<card_id>/like
# request body from front-end-> whole object of attributes
# ? change syntax
@cards_bp.route("/<card_id>/like", methods=["PUT"])
def update_one_card(card_id):
    card = validate_model_instance(Card, card_id, "card")
    request_body = request.get_json()

    card.update_card(request_body)

    db.session.commit()

    return jsonify(card.to_json()), 200

    
