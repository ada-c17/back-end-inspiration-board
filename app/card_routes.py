from flask import Blueprint, request, jsonify, make_response, abort
from flask import Blueprint, abort, request, jsonify, make_response
from app import db
from app.models.card import Card

card_bp = Blueprint("card_bp", __name__, url_prefix="/cards")

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


# GET /boards/<board_id>/cards
@card_bp.route('/boards/<board_id>/cards', methods=['GET'])
def get_all_cards_for_specific_board(board_id):
    board = validate_board(board_id)

    card_list = []

    for card in board.cards:
        card_list.append(card.to_dict())

    return jsonify({
        'id': board.board_id,
        'message': board.message
    }), 200


# POST /boards/<board_id>/cards
@card_bp.route('/boards/<board_id>/cards', methods=['POST'])
def assign_cards_to_board(board_id):
    board = validate_board(board_id)

    request_body = request.get_json()

    card_list = request_body["card_ids"]

    for card in card_list:
        valid_card = validate_card(card)
        board.cards.append(valid_card)
    db.session.commit()

    return jsonify({
        'id': board.board_id,
        'card_ids': card_list
    }), 200


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
