from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card

cards_bp = Blueprint('cards', __name__, url_prefix="/cards")




#DELETE a card
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_one_card(card_id):
    card = Card.query.get(card_id)
    if not card:
        return {"message": f"Card {card_id} not found"}, 404

    db.session.delete(card)
    db.session.commit()

    return jsonify({"details": f"Card {card.card_id} successfully deleted"}), 200

#UPDATE likes "+1" for a card
@cards_bp.route("/<card_id>", methods=["PATCH"])
def update_likes_for_one_card(card_id):
    card = Card.query.get(card_id)
    if not card:
        return {"message": f"Card {card_id} not found"}, 404

    card.likes_count += 1
    db.session.commit()

    return jsonify({"likes_count": card.likes_count}), 200