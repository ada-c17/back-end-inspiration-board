import re
from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
from app.models.board import Board

def handle_id_request(id, db):
    try:
        id = int(id)
    except:
        abort(make_response({"msg": f"Invalid {db.__name__} ID '{id}'."}, 400))

    query = db.query.get(id)

    if not query:
        abort(make_response({"msg": f"{db.__name__} ID '{id}' does not exist."}, 404))

    return query

def validate_card_body(card_body):
    expected_elements = ("message", "board_id")
    for element in expected_elements:
        print(len(element))
        if element not in card_body:
            abort(
                make_response({"msg": f"Invalid data: Missing {element}"},400)
            )
        elif len(card_body["message"]) > 40:
            abort(
                make_response({"msg": f"Invalid data: Message longer than 40 characters"},400)
            )
    return card_body


cards_bp = Blueprint('cards', __name__, url_prefix="/cards")

@cards_bp.route("", methods=["POST"])
def create_new_card():
    request_body = validate_card_body(request.get_json())
    
    handle_id_request(request_body["board_id"], Board)

    new_card = Card(
        message = request_body["message"],
        board_id = request_body["board_id"],
        likes_count = 0
    )
    
    db.session.add(new_card)
    db.session.commit()

    confirmation_msg = jsonify(f"New card #{new_card.card_id} successfully created")
    return make_response(confirmation_msg, 201)


@cards_bp.route("/board/<board_id>", methods=["GET"])
def get_cards_by_board(board_id):
    active_board = handle_id_request(board_id, Board)
    cards = active_board.cards

    response_msg = []
    for card in cards:
        response_msg.append(card.to_dict())

    response_msg = jsonify(response_msg)
    return make_response(response_msg, 200)

@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card_by_id(card_id):
    active_card = handle_id_request(card_id, Card)

    db.session.delete(active_card)
    db.session.commit()

    confirmation_msg = jsonify({"details": f"Card {card_id} successfully deleted."})
    return make_response(confirmation_msg, 200)

@cards_bp.route("/<card_id>/like", methods=["PATCH"])
def like_card_by_id(card_id):
    active_card = handle_id_request(card_id, Card)
    active_card.likes_count = active_card.likes_count + 1
    db.session.commit()

    confirmation_msg = jsonify({"card": active_card.to_dict()})
    return(make_response(confirmation_msg, 200))

#### OPTIONAL: Separate like/unlike patch routes?
@cards_bp.route("/<card_id>/unlike", methods=["PATCH"])
def unlike_card_by_id(card_id):
    pass