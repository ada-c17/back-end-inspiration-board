from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card


card_bp = Blueprint('card_bp', __name__, url_prefix='/cards')


# Validation of Cards helper function
def validate_card(card_id):
    
    try:
        card_id = int(card_id)
    
    except:
        abort(make_response({'message': f'Card {card_id} invalid'}, 400))

    card = Card.query.get(card_id)

    if not card:
        abort(make_response({'message': f'Card {card_id} not found'}, 404))

    return card


# DELETE ONE specific Card
@card_bp.route('/<card_id>', methods=['DELETE'])
def delete_card(card_id):
    card = validate_card(card_id)

    db.session.delete(card)
    db.session.commit()

    return{'details': f'Card {card.card_id} was successfully deleted'}, 200


# UPDATE Card likes
@card_bp.route('/<card_id>/like', methods=['PATCH'])
def like_card(card_id):
    card = validate_card(card_id)
    
    request_body = request.get_json()
    card.likes_count = request_body['likes_count']

    db.session.commit()
    return jsonify(f'Card {card_id} updated likes'), 200
