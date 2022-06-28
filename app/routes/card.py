from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
cards_bp = Blueprint('cards', __name__, url_prefix="/cards")

@cards_bp.route("", methods=["POST"])
def create_new_card():
    request_body = request.get_json()
    new_card = Card(
        message = request_body["message"],
        likes_count = 0
    )

    response = make_response(f"New card #{id} successfully created",
    201)

    pass

@cards_bp.route("/<board_id>", methods=["GET"])
def get_cards_by_board(board_id):
    pass

@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card_by_id(card_id):
    pass

@cards_bp.route("/<card_id>/like", methods=["PATCH"])
def like_card_by_id(card_id):
    pass

#### OPTIONAL: Separate like/unlike patch routes?
@cards_bp.route("/<card_id>/unlike", methods=["PATCH"])
def unlike_card_by_id(card_id):
    pass