from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
from app.models.board import Board

card_bp = Blueprint('cards', __name__, url_prefix="/boards/<my_board_id>/cards")

@card_bp.route("", methods=["POST"])
def create_one_card_for_a_board(my_board_id):
    request_body = request.get_json()
    if "message" not in request_body:
        return jsonify(
            {
                "details": "Please enter a card message!"
            }), 400
    elif "likes_count" not in request_body:
        new_card = Card(message=request_body["message"], likes_count = 0, board_id = my_board_id)
    else:
        new_card = Card(message=request_body["message"], likes_count = request_body["likes_count"], board_id = my_board_id)

    db.session.add(new_card)
    db.session.commit()

    return make_response(jsonify(f"Card with id {new_card.card_id} succesfully created"), 201)

@card_bp.route("", methods=["GET"])
def get_cards_for_specific_board(my_board_id):
    board = validate_and_return_item(Board, my_board_id)

    cards = []
    for card in board.cards:
        cards.append({
        "card_id":card.card_id,
        "message": card.message,
    "likes_count":card.likes_count,
    "board_id": my_board_id
})
    return jsonify({
        "board_id": board.board_id,
        "title": board.title,
        "owner": board.owner,
        "cards": cards
        }), 200

def validate_and_return_item(cls, item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        abort(make_response(jsonify({"details": "Invalid data"})), 400)
    item = cls.query.get(item_id)
    if item:
        return item
    abort(make_response({"details": "Item not found"}, 404))

@card_bp.route("/<card_id>/likes", methods=["PATCH"])
def increase_number_of_likes_with_id(my_board_id, card_id):
    card = validate_and_return_item(Card, card_id)

    card.likes_count = card.likes_count + 1

    db.session.commit()
    return jsonify({'msg': f'Increased the number of likes for card with id {card_id}: {card.likes_count}'})

@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_one_card(my_board_id, card_id):
    board = validate_and_return_item(Board, my_board_id)
    card = validate_and_return_item(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    return jsonify({'msg': f'Deleted card with id {card_id}'})
