from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint('board_bp', __name__, url_prefix='/boards')
card_bp = Blueprint('card_bp', __name__, url_prefix='/cards')

#create a new board using "title" and "owner" inputs

    #see error message if title or owner is blank/empty/invalid/missing

#read: view list of all boards; select a board
@board_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()

    response = []
    for board in boards:
        response.append(board.to_dict())
    
    return jsonify(response), 200

@board_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    chosen_board = Board.query.get(board_id)
    return jsonify(chosen_board.to_dict()), 200

@board_bp.route("", methods=["POST"])
def post_board():
    request_body = request.get_json()

    if "title" in request_body and "owner" in request_body:
        new_board = Board(title=request_body["title"],
                    owner=request_body["owner"])
    else:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_board)
    db.session.commit()

    return make_response({"board": new_board.to_dict()}, 201)


#read: view list of all cards; select a card
@card_bp.route("", methods=["GET"])
def get_all_cards():
    cards = Card.query.all()
    response = []
    for card in cards:
        response.append(card.to_dict())
    return jsonify(response), 200