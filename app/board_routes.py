from flask import Blueprint, request, jsonify, make_response, abort
from app.models.board import Board
from app.models.card import Card
from app import db
from sqlalchemy import asc, desc
from app.models.card import Card

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

# Creat a board
@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    if "title" not in request_body or "owner" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_board = Board(
        title = request_body["title"],
        owner = request_body["owner"])
    db.session.add(new_board)
    db.session.commit()
    return jsonify(new_board.to_dict_board()), 201

# Get all boards 
@boards_bp.route("", methods = ["GET"])
def get_all_boards():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        boards = Board.query.order_by(asc(Board.title))
    elif sort_query == "desc":
        boards = Board.query.order_by(desc(Board.title))
    else:
        boards = Board.query.all()
    return jsonify([board.to_dict_board() for board in boards]), 200

# get one board
@boards_bp.route("/<board_id>", methods= ["GET"])
def get_one_board(board_id):
    board = get_board_or_abort(board_id)
    return jsonify({"board":board.to_dict_board()}), 200

# update a board by id
@boards_bp.route("/<board_id>", methods=["PUT"])
def update_board(board_id):
    chosen_board = get_board_or_abort(board_id)
    request_board = validate_key()
    chosen_board.title = request_board["title"]
    chosen_board.owner = request_board["owner"]
    db.session.add(chosen_board)
    db.session.commit()
    return jsonify(chosen_board.to_dict_board()), 200

# creat card by specific board id
@boards_bp.route("/<board_id>/cards", methods=["POST"])
def create_card_by_board(board_id):
    chosen_board = get_board_or_abort(board_id)
    request_card = validate_key_card()

    new_card = Card(
        message = request_card["message"],
        likes_count = 0,
        board_id = chosen_board.board_id
    )
    db.session.add(new_card)
    db.session.commit()
    return jsonify(new_card.card_response_dict()), 201

# get all cards belong specific borad id
@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_cards_by_board(board_id):
    chosen_board = get_board_or_abort(board_id)
    response_body = [card.card_response_dict() for card in chosen_board.cards]
    return jsonify(response_body), 200

# Helper Function
def validate_key():
    request_board = request.get_json()
    if "title" not in request_board or "owner" not in request_board:
        abort(make_response({"details": "Invalid data"}, 400))
    return request_board

# Helper Function
def get_board_or_abort(board_id):
    try:
        board_id = int(board_id)
    except ValueError:
        abort(make_response({"message": f"The board id {board_id} is invalid. The id must be integer."}, 400))
    
    boards = Board.query.all()
    for board in boards:
        if board.board_id == board_id:
            return board
    abort(make_response({"message": f"The board id {board_id} is not found"}, 404))

# helper function for validating card id
def get_card_or_abort(card_id):
    try:
        card_id = int(card_id)
    except ValueError:
        abort(make_response({"message": f"The card id {card_id} is invalid. The id must be integer."}, 400))
    
    cards = Card.query.all()
    for card in cards: 
        if card.card_id == card_id:
            return card
        else:
            abort(make_response({"message": f"The card id {card_id} is not found"}, 404))

# validating for input of card
def validate_key_card():
    request_card = request.get_json()
    if "message" not in request_card:
        abort(make_response({"details": "Invalid data"}, 400))
    elif len(request_card["message"]) > 40:
        abort(make_response({"details": "Message must be less than 40 characters"}, 400))

    return request_card
