from crypt import methods
import json
from attr import validate
from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card

card_bp = Blueprint("card", __name__, url_prefix="/cards")

@card_bp.route("", methods=["GET"])
def get_cards():
    cards = Card.query.all()
    cards_response = []

    for card in cards:
        cards_response.append({
            "id": card.id,
            "message": card.message,
            "likes_count": card.likes_count
        })
    
    return make_response(jsonify(cards_response), 200)


@card_bp.route("/<int:id>", methods=["GET"])
def get_card(id):
    # card = validate_item(id)

    return jsonify({"card": card.to_json()}), 200


@card_bp.route("", methods=["POST"])
def create_card():
    request_body = request.get_json()

    try:
        new_card = Card(
            message = request_body["message"],
            likes_count = request_body["likes_count"]
        )

    except KeyError:
        return make_response({"details": "Invalid Data"}, 400)

    db.session.add(new_card)
    db.session.commit()

    return jsonify({"card": new_card.to_json()}, 201)


@card_bp.route("/<int:id>", methods=["GET"])
def update_card(id):
    # card = validate_item(id)
    request_body = request.get_json()

    card.message = request_body["message"]

    db.session.commit()

    return jsonify({"card": card.to_json()}, 200)