from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card

card_bp = Blueprint("card_bp", __name__, url_prefix="/cards")

#Validation of cards helper function
def validate_card(card_id):
    card_id-int(card_id)
    cards = Card.query.all()
    for card in cards:
        if card_id==cards.card_id:
            return card
    abort(make_response({'details': 'This card does not exist'}, 404))



# GET /boards/<board_id>/cards

# POST /boards/<board_id>/cards

# DELETE /cards/<card_id>

@card_bp.route('/<card_id>',methods = ['DELETE'])
def delete_card(card_id):
    validate_card(card_id)
    chosen_card = Card.query.get(card_id)
    
    db.session.delete(chosen_card)
    db.session.commit()

    return{'details':f'Card {chosen_card.card_id} "{chosen_card.title}" successfully deleted'}, 200



# PUT /cards/<card_id>/like
