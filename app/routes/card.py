from flask import Blueprint, request, jsonify, make_response, abort
from app import db
import requests
import sqlalchemy
from app import db
from app.models.card import Card
import sqlalchemy

card_bp = Blueprint("card_bp", __name__, url_prefix="/cards")

def validate_id(card_id):
    try:
        card_id = int(card_id)
    except ValueError:
        rsp = {"msg": f"Invalid id: {card_id}"}
        abort(make_response(jsonify(rsp), 400))
    chosen_card = Card.query.get(card_id)

    if chosen_card is None:
        rsp = {"msg": f"Could not find task with id {card_id}"}
        abort(make_response(jsonify(rsp), 404))
    return chosen_card


@card_bp.route("", methods=["POST"])
def create_new_task():
    request_body = request.get_json()

    try:
        message = request_body["message"]
        board_id = request_body["board_id"]
    except KeyError:
        return {"details": "Invalid data"}, 400

    new_card = Card(
        board_id=request_body["board_id"],
        message=request_body["message"],
        #likes_count = request_body["likes_count"]
    )
    
    db.session.add(new_card)
    db.session.commit()
    
    response = {"card": new_card.to_dict()}
    return jsonify(response), 201

@card_bp.route("", methods=["GET"])
def get_all_cards():
    response = []
    cards = Card.query.all()
    for card in cards:
        response.append(
            card.to_dict()
        )
    return jsonify(response)