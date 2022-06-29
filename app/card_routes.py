from email import message
from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# Create a card - MA
@cards_bp.route("", methods=["POST"])
def create_card():
    request_body = request.get_json()

    new_card = Card(
        message=request_body["message"],
        likes_count=0, 
        # board_id=request_body["board_id"]
    )

    db.session.add(new_card)
    db.session.commit()

    return jsonify({"msg": f"Card added"}), 201

# Get all cards route - MA
@cards_bp.route("", methods=["GET"])
def get_all_cards():
    response = []

    cards = Card.query.all()
    for card in cards:
        response.append(
            card.to_dict()
            )

    return jsonify(response)

# Delete card route - MA
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_one_card(card_id):
    try: 
        card_id = int(card_id)
    except ValueError: 
        return jsonify({"msg": f"Invalid card id '{card_id}' - id must be integer"}), 400

    chosen_card = Card.query.get(card_id)

    if chosen_card is None: 
        return jsonify({"msg": f"Could not find with id {card_id}"}), 404

    db.session.delete(chosen_card)
    db.session.commit()

    return jsonify({"msg": f"Deleted card with id {card_id}"})