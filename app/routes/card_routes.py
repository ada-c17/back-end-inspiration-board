from flask import Blueprint, request, make_response, abort
from app import db
from app.external import slack
from app.models.card import Card

card_bp = Blueprint("card", __name__, url_prefix="/cards")

def get_card(card_id):
    try:
        card_id = int(card_id)
    except ValueError:
        abort(make_response({"message": f"The card id {card_id} is invalid. The id must be integer."}, 400))
    
    board = Card.query.get(card_id)
    if not board:
        abort(make_response({"message": f"The card id {card_id} is not found"}, 404))

    return board

@card_bp.route("", methods=["POST"])
def create_card():
    request_body = request.get_json()

    try:
        new_card = Card(
            message = request_body["message"],
            board_id = request_body["board_id"],
            likes_count = 0
        )

    except KeyError:
        return make_response({"details": "Invalid Data"}, 400)

    db.session.add(new_card)
    db.session.commit()

    slack.notify_card_created(new_card.message)

    return make_response({"card": new_card.to_dict()}, 201)

@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_a_card(card_id):
    card = get_card(card_id)

    db.session.delete(card)
    db.session.commit()

    return make_response({'details':f'Card {card.card_id} "{card.message}" successfully deleted'}, 200)

@card_bp.route("/add-like/<card_id>", methods=["PATCH"])
def add_like(card_id):
    card = get_card(card_id)

    card.likes_count += 1

    db.session.commit()

    return make_response({"card": card.to_dict()}, 200)