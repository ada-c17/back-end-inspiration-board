from app import db
from app.models.card import Card
from flask import Blueprint, request, jsonify, make_response, abort
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# CREATE aka POST new card at endpoint: /cards
@cards_bp.route("", methods=["POST"])
def create_card():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return make_response(jsonify(dict(details="Invalid data")), 400)
    
    new_card = Card.create(request_body)
    
    db.session.add(new_card)
    db.session.commit()
    
    return jsonify({"card": new_card.to_dict()}), 201   

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

    return jsonify({'details': f'Card {id} "{card.title}" successfully deleted'}), 200
  
#########   
# PATCH a card at endpoint: cards/id  #Remember PATCH is just altering one or some attributes whereas PUT replaces a record. 
@cards_bp.route("/<id>", methods=["PATCH"])
def update_one_card(id):
    card = validate_card(id)
    request_body = request.get_json()
    card_keys = request_body.keys()

    if "likes_count" in card_keys:
        card.likes_count = request_body["likes_count"]
    # if "message" in card_keys:
    #     card.message = request_body["message"]

    db.session.commit()
    return make_response(f"Card# {card.card_id} successfully updated"), 200

#QUALITY CONTROL HELPER FUNCTION
def validate_card(id):
    try:
        id = int(id)
    except ValueError: 
        abort(make_response(jsonify(dict(details=f"invalid id: {id}")), 400))

    card = Card.query.get(id)
    if card:
        return card

    elif not card:
        abort(make_response(jsonify(dict(message= f"card {id} not found")), 404))
