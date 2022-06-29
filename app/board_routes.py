from flask import Blueprint, request, jsonify, make_response, abort
from app.models.board import Board
from app.models.card import Card
from app import db
from sqlalchemy import asc, desc


boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

def validate_key():
    request_board = request.get_json()
    if "title" not in request_board or "owner" not in request_board:
        abort(make_response({"details": "Invalid data"}, 400))
    return request_board

# helper function for validate id
def get_board_or_abort(board_id):
    try:
        board_id = int(board_id)
    except ValueError:
        abort(make_response({"message": f"The task id {board_id} is invalid. The id must be integer."}, 400))
    
    boards = Board.query.all()
    for board in boards:
        if board.board_id == board_id:
            return board
    abort(make_response({"message": f"The task id {board_id} is not found"}, 404))

@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    if "title" not in request_body or "owner" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_board = Board(
        title = request_body["title"],
        owner = request_body["owner"]
    )

    db.session.add(new_board)
    db.session.commit()
    return jsonify({"board": new_board.to_dict_board()}), 201

# get all elements 
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

@boards_bp.route("<board_id>", methods=["PUT"])
def update_board(board_id):
    chosen_board = get_board_or_abort(board_id)
    request_board = validate_key()
    chosen_board.title = request_board["title"]
    chosen_board.owner = request_board["owner"]
    db.session.add(chosen_board)
    db.session.commit()
    return jsonify({"board": chosen_board.to_dict_board()}), 200


#get one board using Get in routes and accessing by id
@boards_bp.route("/<board_id>", methods= ["GET"])
def get_one_board(board_id):
    board = validate_board(board_id)
    return jsonify({"board":board.to_dict_board()}), 200

# validating board and using as a helper function 
def validate_board(board_id):
    try:
        board_id = int(board_id)
    except ValueError:
        abort(make_response({"message": f"The board id {board_id} is invalid. The id must be integer."}, 400))
    
    boards = Board.query.all()
    for board in boards:
        if board.board_id == board_id:
            return board
    abort(make_response({"message": f"The board id {board_id} is not found"}, 404))

# Add card to board - MA
def validate_card(card_id):
    try: 
        card_id = int(card_id)
    except ValueError:
        abort(make_response(jsonify({"msg": f"Invalid card id: '{card_id}'"}), 400))

    chosen_card = Card.query.get(card_id)

    if chosen_card is None: 
        abort(make_response(jsonify({"msg": f"Could not find card with id {card_id}"}), 404))

    return chosen_card

@boards_bp.route("/<board_id>/cards", methods=["POST"])
def add_cards_to_board(board_id):
    board = validate_board(board_id)

    request_body = request.get_json()
    try: 
        card_ids = request_body["card_ids"]
    except KeyError: 
        return jsonify({"msg": "Missing card_ids in request body"}), 400

    if not isinstance(card_ids, list):
        return jsonify({"msg": "Expected list of card ids"}), 400

    cards = []
    for id in card_ids:
        cards.append(validate_card(id))

    for card in cards: 
        card.board_id = board.board_id

    db.session.commit()

    return jsonify({"msg": f"Added card(s) to board with id {board.board_id}"}), 200
