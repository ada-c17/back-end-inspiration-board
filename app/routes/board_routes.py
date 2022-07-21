from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card
from app.routes.helper import validate_class_instance

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint('board_bp', __name__, url_prefix="/boards")


# ********* BOARD *********
# CREATE new board
# CREATE BOARD - "/boards" - POST
@board_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    try:
        new_board = Board.create(request_body)
    except KeyError:
        return make_response({"details": "Invalid data"}), 400

    db.session.add(new_board)
    db.session.commit()

    return jsonify({"board": new_board.to_json()}), 201


# READ all boards
# GET ALL BOARDS - "/boards" - GET
@board_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()
    boards_response = [board.to_json() for board in boards]

    return jsonify(boards_response), 200


# READ one board
# GET ONE BOARDs - "/boards/1" - GET
@board_bp.route("/<id>", methods=["GET"])
def get_one_board(id):
    board = validate_class_instance(id, Board)

    return jsonify({"board": board.to_json()}), 200


# UPDATE cards
# UPDATE BAORD - "/boards/1" - PUT
@board_bp.route("/<id>", methods=["PUT"])
def update_board(id):
    board = validate_class_instance(id, Board)
    request_body = request.get_json()
    board.update(request_body)

    db.session.commit()

    return jsonify({"board": board.to_json()}), 200


# DELETE board
# UPDATE BAORD - "/boards/1" - DELETE
@board_bp.route("/<id>", methods=["DELETE"])
def delete_board(id):
    board = validate_class_instance(id, Board)

    db.session.delete(board)
    db.session.commit()

    return jsonify({"details": f'Board {id} "{board.title}" successfully deleted'}), 200


# CREATE new card under board ID:
@board_bp.route("/<board_id>/cards", methods=["POST"])
def create_card(board_id):
    request_body = request.get_json()

    new_card = Card.create(board_id, request_body)

    db.session.add(new_card)
    db.session.commit()

    return make_response({"card": new_card.to_json()}, 201)


# GET ALL cards for 1 board:
@board_bp.route("/<board_id>/cards", methods=["GET"])
def get_all_cards(board_id):
    board = validate_class_instance(board_id, Board)
    cards = Card.query.filter_by(board=board)

    return jsonify([{"message": card.message, "like_count": card.like_count, "card_id": card.card_id, "board_id": card.board_id} for card in cards]), 200
