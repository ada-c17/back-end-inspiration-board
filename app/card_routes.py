from app import db
from app.models.card import Card
from flask import Blueprint, jsonify, abort, make_response, request
# from .helper import validate_record, send_message_to_slack
from dotenv import load_dotenv

cards_bp = Blueprint("cards_bp", __name__, url_prefix="/cards")
load_dotenv()

def validate_record(cls, id):
    try:
        id = int(id)
    except ValueError:
        abort(make_response({"message": f"{cls} {id} is invalid"}, 400))

    obj = cls.query.get(id)

    if not obj:
        return abort(make_response({"message": f"{cls.__name__} {id} not found"}, 404))

    return obj


# UPDATE one card
@cards_bp.route("/cards/<card_id>/like", methods=["PUT"])
def update_card(card_id):
    card = validate_record(Card, card_id)
    request_body = request.get_json()

    try:
        card.update(request_body)
    except KeyError:
        return abort(make_response(jsonify({"details":"Invalid data"}), 400))

    db.session.commit()

    return jsonify({'card': card.to_json()}), 200
    

# DELETE one card
@cards_bp.route("/cards/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_record(Card, card_id)
    db.session.delete(card)
    db.session.commit()

    return jsonify({"details":f'Card {card.card_id} successfully deleted'}), 200
