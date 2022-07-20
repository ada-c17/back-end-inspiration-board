from flask import Blueprint, request, jsonify, make_response, abort
from app import db
import requests
import os
from app.models.card import Card
from app.models.board import Board

card_bp = Blueprint('cards', __name__, url_prefix="/boards/<board_id>/cards")


@card_bp.route("", methods=["POST"])
def create_one_card_for_a_board(board_id):
    request_body = request.get_json()
    board = validate_and_return_item(Board, board_id)
    if "message" not in request_body or str(request_body["message"]).split() == []:
        return jsonify(
            {
                "details": "Please enter a card message!"
            }), 400
    elif len(str((request_body["message"]))) > 40:
        return jsonify(
            {
                "details": "Please enter a message that is less than 40 characters!"
            }), 400
    elif "likes_count" not in request_body:
        new_card = Card(
            message=request_body["message"], likes_count=0, board_id=board_id)
    elif not type(request_body["likes_count"]) is int:
        return jsonify(
            {
                "details": "Please enter a number for the likes_count!"
            }), 400
    else:
        new_card = Card(
            message=request_body["message"], likes_count=request_body["likes_count"], board_id=board_id)

    send_slack_notification()

    db.session.add(new_card)
    db.session.commit()

    return make_response(jsonify(f"Card with id {new_card.card_id} succesfully created"), 201)


def send_slack_notification():
    message = "Wow! Someone just created a card!🙂"
    query = {"channel": "ada-bot", "text": f'{message}'}
    headers = {"Authorization": os.environ.get("SLACK_TOKEN")}
    requests.get("https://slack.com/api/chat.postMessage",
                 headers=headers, params=query)


@card_bp.route("", methods=["GET"])
def get_cards_for_specific_board(board_id):
    board = validate_and_return_item(Board, board_id)
    params = request.args

    if "sort" in params:
        if params["sort"] == "asc_alpha":
            sort_by = Card.message.asc()
        elif params["sort"] == "asc_id":
            sort_by = Card.card_id.asc()
        elif params["sort"] == "asc_likes":
            sort_by = Card.likes_count.asc()
        cards = db.session.query(Card).filter_by(board_id=board.board_id).order_by(sort_by).all()
    else:
        cards = board.cards

    response = []
    for card in cards:
        response.append({
            "card_id": card.card_id,
            "message": card.message,
            "likes_count": card.likes_count,
            "board_id": board_id
        })
    return jsonify({
        "board_id": board.board_id,
        "cards": response
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
def increase_number_of_likes_with_id(board_id, card_id):
    card = validate_and_return_item(Card, card_id)
    board = validate_and_return_item(Board, board_id)

    card.likes_count = card.likes_count + 1

    db.session.commit()
    return jsonify({'msg': f'Increased the number of likes for card with id {card_id}: {card.likes_count}'})


@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_one_card(board_id, card_id):
    board = validate_and_return_item(Board, board_id)
    card = validate_and_return_item(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    return jsonify({'msg': f'Deleted card with id {card_id}'})
