from email import message
from flask import Blueprint, request, jsonify, make_response, abort
from app import db

from app.models.board import Board
from app.models.card import Card
from .card_routes import create_card, validate_card

from datetime import datetime

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

# CREATE aka POST new board at endpoint: /boards
@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response(jsonify(dict(details="Invalid data")), 400)
    
    new_board = Board.create(request_body)
    
    db.session.add(new_board)
    db.session.commit()

    return make_response(jsonify({"board": new_board.to_dict()}), 201)   

#######

#app/board_routes.py
@boards_bp.route("/<board_id>/cards", methods=["POST"])
def create_card_for_board(board_id):
    new_card = {}
    board = validate_board(board_id)   
    
    request_body = request.get_json()    

    new_card = create_card(request_body)
    
    card_id = new_card["card_id"]

    cards_list = []
    card = validate_card(card_id)
    
    
    card.board = board 
    cards_list.append(card.card_id)

    db.session.commit()

    updatedBoard = {
        "board_id": board_id,
        "title": board.title,
        "owner": board.owner,
        "card_id": card_id,
        "message": card.message,
        "likes_count": card.likes_count
    }

    return make_response(jsonify(updatedBoard)), 200

@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_cards_per_board(board_id):

    board = validate_board(board_id)
    cards_info = [card.to_dict() for card in board.cards]

    db.session.commit()

    return make_response(jsonify(cards_info)), 200


# GET ALL boardS aka READ at endpoint /boards
@boards_bp.route("", methods=["GET"])
def read_all_boards():
    boards_response = []

    boards = Board.query.all()

    boards_response = [board.to_dict() for board in boards]

    return jsonify(boards_response)

#####
# GET aka READ board at endpoint: /boards/id 
@boards_bp.route("/<id>", methods=["GET"])
def get_board_by_id(id):
    board = validate_board(id)
   
    return jsonify({"board": board.to_dict()}), 200
    
# DELETE /boards/id
@boards_bp.route("<id>", methods=['DELETE'])
def delete_one_board(id):
    board = validate_board(id)

    db.session.delete(board)
    db.session.commit()
    
    return jsonify({'details': f'Board {id} "{board.title}" successfully deleted'}), 200

#QUALITY CONTROL HELPER FUNCTION
def validate_board(id):
    try:
        id = int(id)
    except ValueError: 
        # return jsonify({}), 400     .....OR
        abort(make_response(jsonify(dict(details=f"invalid id: {id}")), 400))

    board = Board.query.get(id)
    if board:
        return board

    elif not board:
        abort(make_response(jsonify("board not found"), 404))

    




