from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from app.models.board import Board
from .routes_helper import get_record_by_id, make_record_safely

card_bp = Blueprint('card_bp', __name__, url_prefix="/boards/")

# Create new card to board by id
@card_bp.route("<board_id>/cards", methods=["POST"], strict_slashes=False)
def create_card(board_id):
    board = get_record_by_id(Board,board_id)
    
    request_body = request.get_json()
    new_card = make_record_safely(Card, request_body )
    new_card.board = board

    db.session.add(new_card)
    db.session.commit()

    return make_response("Success", 201)

# Delete single card
@card_bp.route("<board_id>/cards/<card_id>", methods=["DELETE"], strict_slashes=False)
def delete_card(board_id, card_id):
    get_record_by_id(Board,board_id)
    card = get_record_by_id(Card,card_id)

    db.session.delete(card)
    db.session.commit()
    return make_response("Card successfully deleted", 200)

# Add one like
@card_bp.route("<board_id>/cards/<card_id>/like", methods=["PATCH"], strict_slashes=False)
def add_like(board_id, card_id):
    get_record_by_id(Board,board_id)
    card = get_record_by_id(Card,card_id)

    card.likes_count += 1

    db.session.commit()
    return make_response("Success", 200)