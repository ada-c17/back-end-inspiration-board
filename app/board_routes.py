from flask import Blueprint, request, jsonify, make_response, abort
from app.models.board import Board
from app.models.card import Card
from app import db
from sqlalchemy import asc, desc

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")


# Create a board
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

# Get one board
@boards_bp.route("/<board_id>", methods= ["GET"])
def get_one_board(board_id):
    board = get_board_or_abort(board_id)
    return jsonify({"board":board.to_dict_board()}), 200

# Update a board
@boards_bp.route("<board_id>", methods=["PUT"])
def update_board(board_id):
    chosen_board = get_board_or_abort(board_id)
    request_board = validate_key()
    chosen_board.title = request_board["title"]
    chosen_board.owner = request_board["owner"]
    db.session.add(chosen_board)
    db.session.commit()
    return jsonify({"board": chosen_board.to_dict_board()}), 200

# Create cards for a particular board
@boards_bp.route("/<board_id>/cards", methods=["POST"])
def create_cards_from_board(board_id):
    board = get_board_or_abort(board_id)
    request_body = request.get_json()

    for card_id in request_body["card_ids"]:
        card = get_card_or_abort(card_id)
        board.cards.append(card)

    db.session.commit()

    return {
        "id": board.board_id,
        "card_ids": request_body["card_ids"]
    }

# Get cards for a particular board
@boards_bp.route("/<board_id>/cards", methods=["GET"])
def read_cards_from_board(board_id):
    board = get_board_or_abort(board_id)

    cards_response = []
    for card in board.cards:
        cards_response.append(board.to_dict_board())
        
    return jsonify({
        "id": board.board_id,
        "title": board.title,
        "owner": cards_response
    })


##################################
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

# Helper Function 
def get_card_or_abort(card_id):
    try:
        card_id = int(card_id)
    except ValueError:
        abort(make_response(jsonify({'msg': f"Invalid card id: '{card_id}'. ID must be an integer"}), 400))

    chosen_card = Card.query.get(card_id)

    if chosen_card is None:
        abort(make_response(jsonify({'msg': f'Could not find card with id {card_id}'}), 404))

    return chosen_card





