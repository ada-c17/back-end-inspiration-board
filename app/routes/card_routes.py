from flask import Blueprint, request, jsonify, abort, make_response
from app import db
from app.models.card import Card
from app.routes.helper_routes import validate_id, validate_request, error_message

cards_bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

@cards_bp.route("/<card_id>/like", methods=["PATCH"])
def like_card(card_id):
    card = validate_id(Card, card_id)
    card.likes += 1
    db.session.commit()
    return make_response(jsonify(card.to_dict()), 200)


@cards_bp.route("", methods=['POST'])
def create_card():
    """
    Create a new card
    """
    data = request.get_json()
    try:
        card = Card(message = data['message'], board_id = data['board_id'], likes = data['likes'])
    except KeyError:
        error_message('Invalid data', 400)
    db.session.add(card)
    db.session.commit()
    return jsonify(card.to_dict())

@cards_bp.route("/<card_id>", methods=['DELETE'])
def delete_card(card_id):
    card = validate_id(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    return make_response({"details": f'Card {card.card_id} {card.message} successfully deleted'})



