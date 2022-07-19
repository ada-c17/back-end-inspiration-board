from email import message
from flask import Blueprint, request, jsonify, make_response, abort
from app.models.board import Board
from app.models.card import Card
import requests
import os
from app import db

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")


# helper function to validate board
def validate_board(board_id):
    try:
        board_id = int(board_id)
    except:
        abort(make_response({"message":f"Board ID {board_id} is invalid"}, 400))

    board = Board.query.get(board_id)

    if not board:
        abort(make_response({"message":f"Board ID {board_id} not found"}, 404))

    return board

# routes
@boards_bp.route("", methods = ["POST"])
def create_board():
    request_body = request.get_json()

    if "title" not in request_body or "owner" not in request_body:
        return {"details": "Invalid data"}, 400

    new_board = Board(title=request_body["title"], owner=request_body["owner"])
    db.session.add(new_board)
    db.session.commit()

    # Send notification in Slack
    requests.post('https://slack.com/api/chat.postMessage',
        params={
            'channel':'end-of-the-alphabet', 
            'text': "Someone just created a new card!",
        }, headers={
            'authorization': f'Bearer {os.environ.get("ENVIRONMENT_VARAIBLE_SLACK_TOKEN")}'
        }
    )


    return make_response({"board":new_board.to_json()}, 201)

@boards_bp.route("", methods = ["GET"])
def get_all_boards():
    boards = Board.query.all()

    boards_response = []
    for board in boards:
        boards_response.append(board.to_json())
    
    return jsonify(boards_response)

@boards_bp.route("/<board_id>", methods = ["DELETE"])
def delete_one_board(board_id):
    chosen_board = validate_board(board_id)

    db.session.delete(chosen_board)
    db.session.commit()

    return jsonify({"message": f"Deleted board with id {board_id}"})

@boards_bp.route("/<board_id>", methods = ["GET"])
def get_one_board(board_id):
    board = validate_board(board_id)

    return make_response({"board":board.to_json()}, 200)

@boards_bp.route("/<board_id>/cards", methods = ["GET"])
def get_cards_by_board(board_id):
    board = validate_board(board_id)
    cards_response = []

    for card in board.cards:
        cards_response.append({
            "board_id":board.board_id,
            "id":card.card_id,
            "message": card.message,
            "likes_count": card.likes_count
            })

    return make_response({"cards":cards_response}, 201)


# routes for card
@cards_bp.route("", methods = ["POST"])
def add_card():
    request_body = request.get_json()
    if "message" not in request_body or "board_id" not in request_body:
        return {"details": "Invalid data"}, 400
    
    if len(request_body["message"]) == 0 or len(request_body["message"]) > 40:
        return {"details": "Input message must be between 1 and 40 characters"}, 400

    new_card = Card(message = request_body["message"],
                board_id = int(request_body["board_id"]),
                likes_count = 0)

    db.session.add(new_card)
    db.session.commit()

    rsp = new_card.to_json()
    
    return make_response({"board":rsp}, 201)

@cards_bp.route("", methods = ["GET"])
def get_all_cards():
    cards = Card.query.all()

    cards_response = []
    for card in cards:
        cards_response.append(card.to_json())
    
    return jsonify(cards_response)


# Helper function to validate card   

def validate_card(card_id):
    try:
        card_id = int(card_id)
    except:
        abort(make_response({"message":f"Card ID {card_id} is invalid"}, 400))

    card = Card.query.get(card_id)

    if not card:
        abort(make_response({"message":f"Card ID {card_id} not found"}, 404))

    return card

# Delete cards

@cards_bp.route("/<card_id>", methods = ["DELETE"])
def delete_one_card(card_id):
    chosen_card = validate_card(card_id)

    db.session.delete(chosen_card)
    db.session.commit()

    return jsonify({"message": f"Deleted card with id {card_id}"})


# Update like for cards
@cards_bp.route("/<card_id>/updatelike", methods=["PATCH"])
def update_likes_with_id(card_id):
    chosen_card = validate_card(card_id)
    chosen_card.likes_count += 1

    db.session.commit()
    return jsonify({'msg': f'Update likes with id {card_id} to {chosen_card.likes_count}'})
