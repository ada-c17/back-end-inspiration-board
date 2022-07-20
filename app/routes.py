from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
from app.models.board import Board
import requests
import os
from dotenv import load_dotenv

load_dotenv()

PATH = "https://slack.com/api/chat.postMessage"
API_KEY = os.environ.get("SLACK_TOKEN")

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint("board_bp", __name__, url_prefix="/boards")
card_bp = Blueprint("card_bp", __name__, url_prefix="/cards")

def create_slack_api_request(chosen_card):
    params = {
        "text": f"Someone just wrote a new message {chosen_card.message}",
        "channel": "board-notification"
        }
    hdrs = {
        "Authorization": f"Bearer {API_KEY}"
    }
    r = requests.post(PATH, data = params, headers = hdrs)
    return r

def validate_board(board_id):
    try:
        board = int(board_id)
    except ValueError:
        response = {"msg": f"Invalid id: {board_id}"}
        abort(make_response(jsonify(response), 400))
    chosen_board = Board.query.get(board_id)

    if chosen_board is None:
        response = {"msg": f"Could not find board with id #{board_id}"}
        abort(make_response(jsonify(response), 400))
    return chosen_board

def validate_card(card_id):
    try:
        card = int(card_id)
    except ValueError:
        response = {"msg": f"Invalid id: {card_id}"}
        abort(make_response(jsonify(response), 400))
    chosen_card = Card.query.get(card_id)

    if chosen_card is None:
        response = {"msg": f"Could not find board with id #{card_id}"}
        abort(make_response(jsonify(response), 400))
    return chosen_card

@board_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()
    board_response = []
    for board in boards:
        board_response.append({
            "id": board.board_id,
            "title": board.title,
            "owner": board.owner,
        })
    return jsonify(board_response), 200


@board_bp.route("", methods=["POST"])
def create_one_board():
    request_body = request.get_json()
    try:
        if len(request_body["title"])<1 or len(request_body["owner"])<1:
            abort(make_response(jsonify({"msg": "board must have a title and owner"}), 400))
        if request_body["title"].isspace():
            abort(make_response(jsonify({"msg": "board title must contain numbers or letters"}), 400))
        if request_body["owner"].isspace():
            abort(make_response(jsonify({"msg": "board owner must contain numbers or letters"}), 400))
        new_board = Board(
            title=request_body["title"], owner=request_body["owner"])
    except KeyError:
        return {"msg": "Invalid input"}, 400
        # abort(make_response(jsonify(response), 400))
    db.session.add(new_board)
    db.session.commit()
    response = {"board": {"id": new_board.board_id, "title": new_board.title, "owner": new_board.owner}}
    return jsonify(response), 201


@board_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    chosen_board = validate_board(board_id)
    response = {"board": {
        "id": chosen_board.board_id,
        "title": chosen_board.title,
        "owner": chosen_board.owner,
    }}
    return jsonify(response), 200


@board_bp.route("/<board_id>/cards", methods=["GET"])
def get_cards_from_one_board(board_id):
    chosen_board = validate_board(board_id)
    response = {
        "board_id": chosen_board.board_id,
        "board_title": chosen_board.title,
        "cards": []
    }
    for card in chosen_board.cards:
        response["cards"].append({
            "card_id": card.card_id,
            "board_id": chosen_board.board_id,
            "message": card.message,
            "likes": card.likes_count
        })
    return jsonify(response), 200


@board_bp.route("/<board_id>/cards", methods=["POST"])
def create_one_card(board_id):
    validate_board(board_id)
    request_body = request.get_json()
    try:
        new_message = request_body["message"]
        if len(new_message) > 40 or not new_message:
            abort(make_response(jsonify({"msg": "invalid card message"}), 400))
        new_card = Card(
            message=request_body["message"], likes_count=0, board_id=board_id)
    except KeyError:
        return {"msg": "Invalid input"}, 400
    db.session.add(new_card)
    create_slack_api_request(new_card)
    db.session.commit()
    response = {"card": {"message": new_card.message, "id": new_card.card_id}}
    return jsonify(response), 201


@card_bp.route("/<card_id>", methods=["PATCH"])
def update_card_likecount(card_id):
    card = validate_card(card_id)
    card.likes_count += 1
    db.session.commit()

    response = {"msg": f"update like count to {card.likes_count}"}
    return jsonify(response), 200


@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_one_card(card_id):
    card = validate_card(card_id)
    db.session.delete(card)
    db.session.commit()

    response = {"msg": f"delete card with id: {card.card_id}"}
    return jsonify(response), 200

@board_bp.route("/<board_id>", methods=["DELETE"])
def delete_one_board(board_id):
    board = validate_board(board_id)
    db.session.delete(board)
    db.session.commit()

    response = {"msg": f"delete board with id: {board.board_id}"}
    return jsonify(response), 200