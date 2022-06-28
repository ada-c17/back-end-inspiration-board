from app import db
from app.models.card import Card
from flask import Blueprint, jsonify, abort, make_response, request
# from .helper import validate_record, send_message_to_slack
from dotenv import load_dotenv
from .routes import validate_record
cards_bp = Blueprint("cards_bp", __name__, url_prefix="/cards")
load_dotenv()

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# UPDATE one card
@cards_bp.route("/<card_id>/like", methods=["PUT"])
def update_card(card_id):
    card = validate_record(Card, card_id)
    request_body = request.get_json()
    #{likes_count: 5}
    #addition logic done in front end

    try:
        card.update_likes(request_body)
    except KeyError:
        return abort(make_response(jsonify({"details":"Invalid data"}), 400))

    db.session.commit()

    return jsonify({'card': card.to_json()}), 200
    

# DELETE one card
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_record(Card, card_id)
    db.session.delete(card)
    db.session.commit()

    return jsonify({"details":f'Card {card.card_id} successfully deleted'}), 200
