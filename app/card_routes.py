from flask import Blueprint, request, jsonify, make_response, abort
from flask import Blueprint, abort, request, jsonify, make_response
from app import db
from app.models.card import Card

card_bp = Blueprint("card_bp", __name__, url_prefix="/cards")


def validate_card(card_id):
    try:
        card_id = int(card_id)
    except:
        abort(make_response({"message": f"card {card_id} invalid"}, 400))

    card = Card.query.get(card_id)

    if not card:
        abort(make_response({"message": f"card {card_id} not found"}, 404))

    return card


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
