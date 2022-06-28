from flask import Blueprint, request, jsonify, make_response
from app import db
from .helper import validate_card
from app.models.card import Card

# Blueprint:
card_bp = Blueprint('card_bp', __name__, url_prefix="/cards")

# GET ONE card:


# @card_bp.route("/<id>", methods=["GET"])
# def get_one_card(id):
#     card = validate_card(id)

#     return jsonify({"card": card.to_json()}), 200

# UPDATE one card:


@card_bp.route("/<id>", methods=["PATCH"])
def update_card(id):
    card = validate_card(id)
    request_body = request.get_json()
    card.update(request_body)

    db.session.commit()

    return jsonify({"card": card.to_json()}), 200


# DELETE card:
@card_bp.route("/<id>", methods=["DELETE"])
def delete_card(id):
    card = validate_card(id)

    db.session.delete(card)
    db.session.commit()

    return jsonify({"details": f"Card {id} successfully deleted"}), 200
