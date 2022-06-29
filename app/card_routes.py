from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
from app.models.board import Board 
from .board_routes import get_card_or_abort

# example_bp = Blueprint('example_bp', __name__)
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# Delete card route - MA
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_one_card(card_id):
    chosen_card = get_card_or_abort(card_id)
    if chosen_card is None: 
        return jsonify({"msg": f"Could not find with id {card_id}"}), 404

    db.session.delete(chosen_card)
    db.session.commit()
    return jsonify({"msg": f"Deleted card with id {card_id}"})
