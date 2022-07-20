from crypt import methods
from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from .models.board import Board
from .models.card import Card
import requests, os
from dotenv import load_dotenv

boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")
cards_bp = Blueprint("card_bp", __name__, url_prefix="/cards")
load_dotenv()

# ****************************
# BOARD ROUTES
# ****************************

# ***** POST /boards *****
@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()

    if not "title" in request_body and not "owner" in request_body or len(request_body["title"]) == 0 and len(request_body["owner"]) == 0:
        return jsonify({
            "details": "Must include title and owner"
        }), 400
    
    if not "title" in request_body or len(request_body["title"]) == 0:
        return jsonify({
            "details": "Must include title"
        }), 400

    if not "owner" in request_body or len(request_body["owner"]) == 0:
        return jsonify({
            "details": "Must include owner"
        }), 400

    new_board = Board(title=request_body["title"], owner=request_body["owner"])

    db.session.add(new_board)
    db.session.commit()

    return {
        "title": new_board.title,
        "owner": new_board.owner
    }, 201

# ***** GET /boards *****
# validate id helper function
def validate_board(board_id):
    try:
        board_id = int(board_id)
    except ValueError:
        rsp = {"details": f"Invalid id: {board_id}"}
        abort(make_response(jsonify(rsp), 400))

    selected_board = Board.query.get(board_id)
    if selected_board is None:
        rsp = {"details": f"Could not find board with ID: {board_id}"}    
        abort(make_response(jsonify(rsp), 404))

    return selected_board    

@boards_bp.route('', methods=['GET'])
def get_all_boards():
    # sort_boards = request.args.get("sort")

    boards = Board.query.all()
    boards_response = [] 

    for board in boards:
        boards_response.append({
            "id": board.board_id,
            "title": board.title,
            "owner": board.owner,
        })

    return jsonify(boards_response), 200    

@boards_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    selected_board = validate_board(board_id)

    rsp = {
        "board_id": selected_board.board_id,
        "title": selected_board.title,
        "owner": selected_board.owner
    }

    return jsonify(rsp), 200


# ***** DELETE /boards *****
@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = validate_board(board_id)

    db.session.delete(board)
    db.session.commit()

    return {
        "details": f"Board {board_id} successfully deleted"
    }, 200


# ****************************
# CARD ROUTES
# ****************************

# ***** MESSAGE SLACK - helper function, sends slack message when card is created *****
SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
def send_slack_message(card):
    PATH = 'https://slack.com/api/chat.postMessage'
    query_params = {
        "channel":"team-farenheit",
        "text":f"New card created for {card.board_id}. Card message: {card.message}"
    }
    header = {"Authorization" : f"Bearer {SLACK_TOKEN}"}

    response = requests.post(PATH, params=query_params, headers=header)
    return response


# ***** POST /boards/<board_id>/cards *****
@boards_bp.route('/<board_id>/cards', methods=["POST"])
def create_one_card(board_id):
    request_body = request.get_json()
    
    if not "message" in request_body or len(request_body["message"]) == 0:
        return jsonify({
            "details": "Must include message"
        }), 400

    if len(request_body["message"]) > 40:
        return jsonify({
            "details": "Message must be under 40 characters"
        }), 400

    new_card = Card(message=request_body["message"], board_id=board_id, likes_count=0)

    db.session.add(new_card)
    db.session.commit()

    #send message to slack channel
    send_slack_message(new_card)

    return {
        "card_id": new_card.card_id, 
        "board_id": new_card.board_id,
        "message": new_card.message,
        "likes_count": new_card.likes_count
    }

# ***** GET /boards/<board_id>/cards *****
@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_all_cards_by_board_id(board_id):
    selected_board = validate_board(board_id)

    cards_response = []

    for card in selected_board.cards: 
        cards_response.append({
            "card_id": card.card_id,
            "message": card.message,
            "likes_count": card.likes_count,
            "board_id": card.board_id
        })
    
    return jsonify(cards_response), 200


# ***** GET /cards *****
@cards_bp.route("", methods=["GET"])
def get_all_cards():
    cards = Card.query.all()
    card_response = []
    for card in cards:
        card_response.append({
            "card_id": card.card_id,
            "message": card.message,
            "likes_count": card.likes_count,
            "board_id": card.board_id
        })
    return jsonify(card_response), 200

# ***** Helper function for Card Validation *****
def validate_card(card_id):
    try:
        card_id = int(card_id)
    except ValueError:
        rsp = {"details": f"Invalid id: {card_id}"}
        abort(make_response(jsonify(rsp), 400))

    selected_card = Card.query.get(card_id)
    if selected_card is None:
        rsp = {"details": f"Could not find card with ID: {card_id}"}    
        abort(make_response(jsonify(rsp), 404))

    return selected_card  

# ***** GET /cards/<card_id> *****
@cards_bp.route("/<card_id>", methods=["GET"])
def get_one_card(card_id):
    selected_card = validate_card(card_id)

    rsp = {
        "card_id": selected_card.card_id,
        "message": selected_card.message,
        "likes_count": selected_card.likes_count,
        "board_id": selected_card.board_id
    }

    return jsonify(rsp), 200

# ***** DELETE /cards/<card_id> *****
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_card(card_id)
    db.session.delete(card)
    db.session.commit()

    return {
        "details": f"Card {card_id} successfully deleted"
    }, 200

# ***** PUT /cards/<card_id>/like *****
@cards_bp.route("/<card_id>/like", methods=["PUT"])
def like_card(card_id):
    card = validate_card(card_id)

    card.likes_count = card.likes_count + 1
    db.session.add(card)
    db.session.commit()

    return {
        "details": f"Card {card_id}'s likes successfully updated"
    }, 200