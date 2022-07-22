from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from .helpers import validate_model_instance, send_slack_new_card_message
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

#CREATE one board
@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()

    new_board = Board.from_json(request_body)

    db.session.add(new_board)
    db.session.commit()

    return jsonify(new_board.to_json()), 201

#GET all boards
@boards_bp.route("", methods=["GET"])
def read_board():
    Boards = Board.query.all()

    boards_response = [board.to_json() for board in Boards]
        
    return jsonify(boards_response), 200

#GET one board
@boards_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    board = validate_model_instance(Board, board_id, "board")
    return jsonify(board.to_json()), 200

#DELETE A BOARD-> optional
@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = validate_model_instance(Board, board_id, "board")
    db.session.delete(board)
    db.session.commit()

    return jsonify({"details":f'Board {board_id} "{board.title}" successfully deleted'} ), 200

#POST /boards/<board_id>/cards
#we expect-> HTTP request body ({message, likesCount, boardId})
@boards_bp.route("/<board_id>/cards", methods=["POST"])
def add_card_to_board(board_id):
    board = validate_model_instance(Board, board_id, "board")
    
    request_body = request.get_json()

    new_card = board.link_card_to_board(request_body)

    db.session.add(new_card)
    db.session.commit()
    send_slack_new_card_message(new_card)
    #change return?
    return jsonify(new_card.to_json()), 200

#GET /boards/<board_id>/cards
@boards_bp.route("/<board_id>/cards", methods=["GET"])
def read_cards_of_board(board_id):

    board = validate_model_instance(Board, board_id, "board")
    board_cards = [card.to_json() for card in board.cards]

    return jsonify({"boardId": board.board_id,
        "title": board.title,
        "owner": board.owner,
        "cards": board_cards}), 200



