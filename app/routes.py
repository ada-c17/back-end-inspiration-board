from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from .models.board import Board
from .models.card import Card

boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

def error_message(message, status_code):
    abort(make_response({"details":message}, status_code))

@boards_bp.route("", methods=["GET"])
def get_boards():
    boards = Board.query.all()
    boards_response = [board.to_dict() for board in boards]

    return jsonify(boards_response)

@boards_bp.route('', methods=['POST'])
def create_board():
    request_body = request.get_json()

    if not "title" in request_body or not "owner" in request_body:  # or \
        error_message('Invalid Data', 400)

    new_board = Board(title=request_body["title"],
                    owner=request_body["owner"]
                    )

    db.session.add(new_board)
    db.session.commit()

    return {
        "board": new_board.to_dict()
    }, 201

@boards_bp.route("/<board_id>", methods=["GET"])
def get_board_by_id(board_id):
    board = Board.validate(board_id)
    return {"board": board.to_dict()}

@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_all_cards_on_board(board_id):

    board = Board.validate(board_id)

    cards = board.cards
    list_of_cards = []
    for card in cards:
        list_of_cards.append(card.to_dict())

    return {"cards": list_of_cards}

@boards_bp.route("/<id>/cards", methods=["POST"])
def add_card_to_board(id):
    board = Board.validate(id)
    
    request_body = request.get_json()

    if not "message" in request_body:
        error_message('Invalid Data', 400)
    
    if (1 > len(request_body["message"])) or (len(request_body["message"]) > 40): 
        error_message("Message must be between 1 and 40 characters", 400)

    new_card = Card(board_id=id,
                message=request_body["message"]
                )
    db.session.add(new_card)
    db.session.commit()

    response_body = new_card.to_dict()
    return make_response(jsonify(response_body), 200)

@boards_bp.route("/<board_id>/cards/<card_id>", methods=["DELETE"])
def delete_card_by_id(board_id, card_id):
    card = Card.validate(card_id)

    db.session.delete(card)
    db.session.commit()

    return make_response(dict(details=f'Card {card.card_id} "{card.message}" successfully deleted'), 200)

@boards_bp.route("/<board_id>/cards/<card_id>", methods = ["PATCH"])
def add_likes_to_card(board_id, card_id):
    board = Board.validate(board_id)
    card = Card.validate(card_id)

    card.likes_count += 1

    db.session.commit()

    return make_response(card.to_dict(), 200)
