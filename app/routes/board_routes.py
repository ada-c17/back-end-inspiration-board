from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card
import requests
import os

boards_bp = Blueprint('boards', __name__, url_prefix="/boards")


#READ all boards
@boards_bp.route("",methods=["GET"])
def read_all_boards():
    boards = Board.query.all()

    # create response body
    boards_response = []
    for board in boards:
        boards_response.append(board.to_json())
    
    return jsonify(boards_response), 200


#CREATE a new board
@boards_bp.route("", methods=["POST"])
def create_new_board():
    request_body = request.get_json()
    if "title" in request_body and "owner" in request_body:
        new_board = Board.create(request_body)
        db.session.add(new_board)
        db.session.commit() 
        return {"board": new_board.to_json()}, 201
    else:
        return {"details": "Invalid data"}, 400

#READ all cards belonging to a board
@boards_bp.route("/<board_id>/cards",methods=["GET"])
def read_all_cards(board_id):
    # validate the selected board  !!!!!!!!!!can build a helper function
    #   1. check if input is valid datatype
    try:
        board_id = int(board_id)
    except:
        abort(make_response({"message": f"Board{board_id} is invalid"}, 400))

    board = Board.query.get(board_id)
    #   2. check if selected board_id exists
    if not board:
        abort(make_response({"message": f"board{board_id} not found"}, 404))

    cards_list = []
    for card in board.cards:
        cards_list.append(card.to_json())

    if request.args.get("sort") == 'likes':
        cards_list.sort(key=lambda x: x.get('likes_count'), reverse=True)
    elif request.args.get("sort") == 'id':
        cards_list.sort(key=lambda x: x.get('card_id'))
    elif request.args.get("sort") == 'letter':
        cards_list.sort(key=lambda x: x.get('message').upper())

    return jsonify(cards_list),200


#CREATE a new card for the selected board 
@boards_bp.route("/<board_id>/cards", methods=["POST"])
def create_new_card(board_id):
    # get the selected board  !!!!!!!!!!!!!can use helper function
    try:
        board_id = int(board_id)
    except:
        abort(make_response({"message": f"Board{board_id} is invalid"}, 400))

    board = Board.query.get(board_id)

    if not board:
        abort(make_response({"message": f"board{board_id} not found"}, 404))

    # get request body from front end
    request_body = request.get_json()
    if "message" in request_body:
        new_card = Card.create(request_body)
        new_card.board = board
        db.session.add(new_card)
        db.session.commit()

        key = os.environ.get("SLACK_API")
        payload = {
            "channel": "bored_at_work",
            "text": f"Someone just added the card \"{new_card.message}\""\
                f" to board {board_id}."
            }
        header = {"Authorization": f"Bearer {key}"}
        requests.post("https://slack.com/api/chat.postMessage", params=payload,
                        headers=header)
        
        return {"card": new_card.to_json()}, 201
    else:
        return {"details": "Invalid data"}, 400