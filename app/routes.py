from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
from app.models.board import Board
import requests

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint("board_bp", __name__, url_prefix="/boards")
card_bp = Blueprint("card_bp", __name__, url_prefix="/cards")

def validate_board(board_id):
    try:
        board = int(board_id)
    except ValueError:
        response = {"msg":f"Invalid id: {board_id}"}
        abort(make_response(jsonify(response), 400))
    chosen_board = Board.query.get(board_id)

    if chosen_board is None:
        response = {"msg":f"Could not find board with id #{board_id}"}
        abort(make_response(jsonify(response), 400))
    return chosen_board


@board_bp.route("", methods = ["GET"])

@board_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()
    board_response = []
    for board in boards:
        board_response.append({
            "id": board.board_id,
            "title": board.title,
            "owner": board.owner,
        })
    return jsonify(board_response), 200


@board_bp.route("", methods=["POST"])
def create_one_board():
    request_body = request.get_json()
    try:
        new_board = Board(
            title=request_body["title"], owner=request_body["owner"])
    except KeyError:
        return {"msg": "Invalid input"}, 400
        # abort(make_response(jsonify(response), 400))
    db.session.add(new_board)
    db.session.commit()
    response = {"board": {"title": new_board.title, "owner": new_board.owner}}
    return jsonify(response), 201

@board_bp.route("/<board_id>", methods = ["GET"])
def get_one_board(board_id):
    chosen_board = validate_board(board_id)
    response = {"board":{
        "id": chosen_board.board_id,
        "title": chosen_board.title,
        "owner": chosen_board.owner,
    }}
    return jsonify(response), 200

@board_bp.route("/<board_id>/cards", methods = ["GET"])
def get_cards_from_one_board(board_id):
    chosen_board = validate_board(board_id)
    response = {
        "board_id": chosen_board.board_id,
        "board_title": chosen_board.title,
        "cards":[]
    }
    for card in chosen_board.cards:
        response["cards"].append({
            "card_id":card.card_id,
            "board_id":chosen_board.board_id,
            "message":card.message
        })
    return jsonify(response), 200

@board_bp.route("/<board_id>/cards", methods=["POST"])
def create_one_card(board_id):
    request_body = request.get_json()
    try:
        new_message = request_body["message"]
        if len(new_message) > 40 or not new_message:
            abort(make_response(jsonify({"msg": "invalid card message"}), 400))
        new_card = Card(
            message=request_body["message"], likes_count=0, board_id=board_id)
    except KeyError:
        return {"msg": "Invalid input"}, 400
    db.session.add(new_card)
    db.session.commit()
    response = {"card":{"message":new_card.message, "id": new_card.card_id}}
    return jsonify(response), 201
    response = {"card": {"message": new_card.message, "id": new_card.card_id}}
    return jsonify(response), 201


@card_bp.route("/<card_id>", methods=["PATCH"])
def update_card_likecount(card_id):
    card = Card.query.get(card_id)
    card.likes_count += 1
    db.session.commit()

    response = {"msg": f"update like count to {card.likes_count}"}
    return jsonify(response), 200

@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_one_card(card_id):
    card = Card.query.get(card_id)
    db.session.delete(card)
    db.session.commit()

    response = {"msg": f"delete card with id: {card.card_id}"}
    return jsonify(response), 200
