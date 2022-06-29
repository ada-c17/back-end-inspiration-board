from email import message
from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card

cards_bp = Blueprint('cards_bp', __name__, url_prefix='/cards')

def validate_or_abort_card(card_id):
    # returns 400 error if invalid card_id (alpha/non-int) 
    try:
        card_id = int(card_id)
    except ValueError:
        abort(make_response({"error": f"{card_id} is an invalid card id"}, 400))
    
    # returns 404 error if card_id not found in database
    card = Card.query.get(card_id)
    if not card:
        abort(make_response({"error": f"card {card_id} not found"}, 404))
    return card


@cards_bp.route('', methods=['GET'])
def get_cards():
    board_query = request.args.get("sort")
    cards = Card.query.all()
    card_response = []
    for card in cards:
        card_response.append(
            {
                "card_id": card.card_id,
                "message": card.message,
                "likes_count": card.likes_count,
                "board_id": card.board_id
            }
        )
    return jsonify(card_response)
    

@cards_bp.route('', methods=['POST'])
def create_card():
    request_body = request.get_json()
    try:
        new_card = Card(
            message=request_body['message'], 
            likes_count=request_body['likes_count'],
            board_id = request_body['board_id']
            )
    except:
        abort(make_response({'details': f'Invalid data'}, 400))
        
    db.session.add(new_card)
    db.session.commit()
    
    return {
        "card_id": new_card.card_id,
        "message": new_card.message,
        "likes_count": new_card.likes_count,
        "board_id": new_card.board_id
    }, 201

@cards_bp.route("/<card_id>", methods=['DELETE'])
def delete_card(card_id):
    card= validate_or_abort_card(card_id)

    db.session.delete(card)
    db.session.commit()
    return {'details': f'Card {card.card_id} successfully deleted'}