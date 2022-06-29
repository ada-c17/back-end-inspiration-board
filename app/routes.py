from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card

boards_bp = Blueprint("boards", __name__, url_prefix="/boards") 

def validate_board(id):
    board = Board.query.get(id)

    if not board:
        abort(make_response({"message": f"board {id} not found"}, 404))

    return board

# Create board
@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()

    try:
        new_board = Board.create(request_body)
    except KeyError:
        return make_response({"details":"Invalid data"}, 400)

    db.session.add(new_board)
    db.session.commit()

    return jsonify({"board":new_board.to_dict()}), 201

# Get board
@boards_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()
    boards_response = [board.to_dict() for board in boards]

    return jsonify(boards_response), 200

# Get one board
@boards_bp.route("/<id>", methods=["GET"])
def get_one_board(id):
    board= validate_board(id)

    return jsonify(board.to_dict()), 200

# Delete board
@boards_bp.route("/<id>", methods=["DELETE"])
def delete_board(id):
    board = validate_board(id)

    db.session.delete(board)
    db.session.commit()

    return jsonify({"details": f'board id:{id}, title:{board.title}, owner:{board.owner} successfully deleted'}), 200
    
# POST boards/board_id/cards
@boards_bp.route("/<board_id>/cards", methods=["POST"])
def creat_card_in_board(board_id):
    request_body = request.get_json()
    board = validate_board(board_id)
    
    try:
        new_card = Card.create_card(request_body)
    except KeyError:
        return make_response({"details":"Invalid data"}, 400)

    board.cards.append(new_card)
    db.session.commit()

    return jsonify(new_card.to_dict()), 201

# GET boards/board_id/cards
@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_cards_by_board_id(board_id):
    board = validate_board(board_id)
    
    response = board.to_dict()
    response["cards"] = []
    for card in board.cards:
        response["cards"].append(card.to_dict())
        
    return jsonify(response), 200