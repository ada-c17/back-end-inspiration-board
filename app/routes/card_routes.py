from app import db
from app.models.card import Card
from flask import Blueprint, request, jsonify, make_response, abort
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# CREATE aka POST new card at endpoint: /cards
# @cards_bp.route("", methods=["POST"])
def create_card(request_body):
    if "message" not in request_body:
        return make_response(jsonify(dict(details="Invalid data")), 400)
    
    added_card = Card.create(request_body)
    
    db.session.add(added_card)
    db.session.commit()
    
    return added_card.to_dict()   

# @cards_bp.route("/<id>", methods=['PUT'])
# def update_card(id):
#     card = validate_card(id)

#     request_body = request.get_json()

#     card.update(request_body)
#     db.session.commit()
#     return jsonify({"card": card.to_dict()}), 200

# DELETE /cards/id
@cards_bp.route("<id>", methods=['DELETE'])
def delete_one_card(id):
    card = validate_card(id)

    db.session.delete(card)
    db.session.commit()

    return jsonify({'details': f'Card {id} "{card.message}" successfully deleted'}), 200
  
#########   
# PATCH a card at endpoint: cards/id  #Remember PATCH is just altering one or some attributes whereas PUT replaces a record. 
@cards_bp.route("/<id>", methods=["PATCH"])
def update_one_card(id):
    card = validate_card(id)
    likes_param = request.args.get("likes_count")
    
    card.likes_count = likes_param    
    db.session.commit()
    response_body = {
            "card_id":{card.card_id}, 
            "likes_count": 0,
            "message": {card.message}
    }
    return card.to_dict(), 200

#QUALITY CONTROL HELPER FUNCTION
def validate_card(card_id):
    try:
        card_id = int(card_id)
    except ValueError: 
        abort(make_response(jsonify(dict(details=f"invalid id: {card_id}")), 400))

    card = Card.query.get(card_id)
    if card:
        return card

    elif not card:
        abort(make_response(jsonify(dict(message= f"card {card_id} not found")), 404))
