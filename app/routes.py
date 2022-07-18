from app.models.board import Board
from app.models.card import Card
from flask import Blueprint, request, jsonify, make_response, abort
from app import db
import requests

# example_bp = Blueprint('example_bp', __name__)

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")



    # ************************************Routes for Boards*************************************
def validate_board(board_id):
    try:
        board_id = int(board_id)
    except:
        abort(make_response({"message":f"board {board_id} invalid"}, 400))

    board = Board.query.get(board_id)

    if not board:
        abort(make_response({"message":f"board {board_id} not found"}, 404))

    return board




#Create one board
@boards_bp.route("", methods=["POST"])
def create_new_board():
    
    request_body = request.get_json()
    if "title" not in request_body or "owner" not in request_body:
        return {"details":f"Invalid data"},400

    new_board = Board(title=request_body["title"],
                    owner=request_body["owner"],
                    )

    db.session.add(new_board)
    db.session.commit()
    return {"board":new_board.to_json()},201





# Read all boards
@boards_bp.route("", methods=["GET"])
def get_boards():

    boards= Board.query.all()
    board_response = []
    
    for board in boards:
        board_response.append(board.to_json())
    
    return jsonify(board_response),200

# Read all cards for a board
@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_cards(board_id):
    board = validate_board(board_id)
    cards = Card.query.filter_by(board=board)############## is there a more direct way
    card_response = []
    
    for card in cards:
        card_response.append(card.to_json())

    return jsonify(card_response),200

#Create one card
@boards_bp.route("/<board_id>/cards", methods=["post"])
def create_new_card(board_id):

    board = validate_board(board_id)
    request_body = request.get_json()
    if "message" not in request_body:
        return {"details": "Invalid data message required."},400
    new_card = Card(message=request_body["message"], board_id=board_id) ##########maybe board_id = board or task.goal_id=goal.goal_id

    db.session.add(new_card)
    db.session.commit()

    return {"card":{"id":new_card.card_id, "message":new_card.message}},201



#Delete one board
@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = validate_board(board_id)

    cards = Card.query.filter_by(board=board)############## is there a more direct way
    
    for card in cards:
        db.session.delete(card)

    db.session.delete(board)
    db.session.commit()

    return {"details":f'Board {board.board_id} \"{board.title}\" successfully deleted'},200


    # ************************************Routes for Cards**************************************

def validate_card(card_id):
    try:
        card_id = int(card_id)
    except:
        abort(make_response({"message":f"card {card_id} invalid"}, 400))

    card = Card.query.get(card_id)

    if not card:
        abort(make_response({"message":f"card {card_id} not found"}, 404))

    return card




#Update one card//?????????????????with heart url/cards/#
@cards_bp.route("/<card_id>", methods=["PUT"])
def update_card(card_id):
    card = validate_card(card_id)

    card.likes_count += 1

    db.session.commit()

    return {"details": f"card #{card.card_id} successfully liked"},200


#Delete one card
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_card(card_id)

    db.session.delete(card)
    db.session.commit()

    return {"details": f"card {card.card_id} \"{card.title}\" successfully deleted"},204

