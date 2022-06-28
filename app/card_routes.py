from flask import Blueprint, request, jsonify, make_response
from app import db
from models import Card

# example_bp = Blueprint('example_bp', __name__)
card_bp = Blueprint('card_bp', __name__, url_prefix="/boards/")

@card_bp.route("<board_id>/cards", methods=["CREATE"], strict_slashes=False)
def create_card(board_id):
    #validate
    request_body = request.get_json()
    new_card = Card(message=request_body["message"], board_id=board_id)

    db.session.add(new_card)
    db.session.commit()

    return make_response("Success", 201)

@card_bp.route("<board_id>/cards/<card_id>", methods=["PATCH"], strict_slashes=False)
def update_card(board_id, card_id):
    #validate board_id
    #validate card_id
    card = Card.query.get(card_id)

    request_body = request.get_json()
    card["message"] = request_body["message"]

    db.session.commit()
    return make_response("Success", 200)