from flask import Blueprint, request, jsonify, make_response, abort
# from flask import Blueprint, abort, request, jsonify, make_response
from app import db
from app.models.card import Card
# from .board_routes import validate_board


card_bp = Blueprint("card_bp", __name__, url_prefix="/cards")

#Not needed? TBD. However, nice for troubleshooting.
@card_bp.route('', methods=['POST'])
def create_a_card():
    request_body = request.get_json()

    card = Card(message=request_body['message'])
    
    db.session.add(card)
    db.session.commit()
    
    return {'card': card.to_dict()}, 201

#Not needed? TBD. However, nice for troubleshooting.
@card_bp.route('', methods=['GET'])
def get_all_cards():
    cards = Card.query.all()
    
    card_list = []
    for card in cards:
        card_list.append(card.to_dict())

    return jsonify(card_list), 200


# Validation of cards helper function
def validate_card(card_id):
    try:
        card_id = int(card_id)
    except:
        abort(make_response({"message": f"card {card_id} invalid"}, 400))

    card = Card.query.get(card_id)

    if not card:
        abort(make_response({"message": f"card {card_id} not found"}, 404))

    return card

# DELETE /cards/<card_id>
@card_bp.route('/<card_id>', methods=['DELETE'])
def delete_card(card_id):
    validate_card(card_id)
    chosen_card = Card.query.get(card_id)

    db.session.delete(chosen_card)
    db.session.commit()

    return{'details': f'Card {chosen_card.card_id} "{chosen_card.title}" successfully deleted'}, 200


# PUT /cards/<card_id>/like
@card_bp.route("/<card_id>", methods=["PUT"])
def like_card(card_id):
    card = validate_card(card_id)

    request_body = request.get_json()

    card.message = request.body["message"]
    card.likes_count = request.body["likes_count"]

    db.session.commit()

    return jsonify(f"Card #{card_id} liked")
