from email import message
from app.models.card import Card
from app import db
from flask import Blueprint, jsonify, make_response, request, abort


cards_bp = Blueprint('cards', __name__, url_prefix="/cards")

def check_request_body():
    request_body = request.get_json()
    if "message" not in request_body or "likes_count" not in request_body:
        abort(make_response({"details": f"invalid data"}, 404))
    return request_body

@cards_bp.route("", methods=["GET"])
def get_cards():
    cards = Card.query.all()
    cards_response = []
    for card in cards:
        cards_response.append(
            {"id":card.card_id,
             "message": card.message,
             "likes_count": card.likes_count
             })
    
    return jsonify(cards_response), 200


def validate_card(card_id):
    try:
        card_id = int(card_id)  
    except ValueError:
        abort(make_response({"msg": f"Invalid card id #{card_id}."}, 400)) 

    valid_id = Card.query.get(card_id)
    if valid_id is None:
        abort(make_response({"msg": f"card id #{card_id} is not found."}, 404))
        
    return valid_id

@cards_bp.route("/<card_id>", methods=["GET"])
def get_one_card(card_id):
    card = validate_card(card_id)

    response = {"id":card.card_id,
                "message": card.message,
                "likes_count": card.likes_count}
    return jsonify(response), 200


@cards_bp.route("", methods=["POST"])
def create_cards():
    request_body = check_request_body()
    new_card = Card(message=request_body["message"], likes_count=request_body["likes_count"])
    db.session.add(new_card)
    db.session.commit()
    
    response = {"id": new_card.card_id,
                "message": new_card.message,
                "likes_count": new_card.likes_count}
    return jsonify(response), 201
    

@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_card(card_id)
    
    db.session.delete(card)
    db.session.commit()
    
    return { "msg": f"Card {card_id} is successfully deleted." }, 200
