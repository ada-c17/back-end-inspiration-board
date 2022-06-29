from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from app.models.board import Board 

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")


# Create a card
@cards_bp.route("", methods = ["POST"])
def create_card(): 
    request_body = request.get_json()
    if "message" not in request_body:
        return {"details": "Invalid data"}, 400
    
    new_card = Card(message=request_body["message"])
    
            
    db.session.add(new_card)
    db.session.commit()
    return jsonify({
        "card": new_card.to_dict()
        }), 201
