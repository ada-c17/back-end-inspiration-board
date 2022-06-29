
from app.models.card import Card
from app import db
from flask import Blueprint, jsonify, make_response, request, abort


cards_bp = Blueprint('cards', __name__, url_prefix="/cards")

def validate_card(card_id):
    try:
        card_id = int(card_id)  
    except ValueError:
        abort(make_response({"msg": f"Invalid card id #{card_id}."}, 400)) 

    valid_id = Card.query.get(card_id)
    if valid_id is None:
        abort(make_response({"msg": f"card id #{card_id} is not found."}, 404))
        
    return valid_id

@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_card(card_id)
    
    db.session.delete(card)
    db.session.commit()
    
    return { "msg": f"Card {card_id} is successfully deleted." }, 200

@cards_bp.route("/<card_id>/like", methods=["PATCH"])
def update_card_likes(card_id):

    card = validate_card(card_id) 
   
    card.likes_count+=1
    db.session.commit() 

    response = card.to_json()

    return jsonify(response), 200


