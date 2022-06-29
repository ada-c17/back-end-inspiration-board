from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
from app.models.board import Board 
from .board_routes import get_card_or_abort

# example_bp = Blueprint('example_bp', __name__)
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# delete card by id
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card_by_id(card_id):
    chosen_card = get_card_or_abort(card_id)
    db.session.delete(chosen_card)
    db.session.commit()
    response_body = {"message": f"Card {chosen_card.card_id} '{chosen_card.message}' successfully deleted"}
    return jsonify(response_body), 200

# update like by card id
@cards_bp.route("/<card_id>/like", methods=["PUT"])
def update_likes_by_card_id(card_id):
    chosen_card = get_card_or_abort(card_id)
    request_card = validate_key_like ()
    chosen_card.likes_count = request_card["likes_count"]
    db.session.commit()
    return jsonify(chosen_card.card_response_dict()), 200

# helper function for validating input key of like
def validate_key_like():
    request_card = request.get_json()
    if "likes_count" not in request_card:
        abort(make_response({"details": "Invalid data"}, 400))
    return request_card
