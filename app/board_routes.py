from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card
from .routes import validate_record

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

@boards_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()
    board_response = []
    board_response = [board.to_json() for board in boards]
    return jsonify(board_response), 200


@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_cards_by_board(board_id):
    board_id = int(board_id)
    board = validate_record(Board, board_id)
    card_list = []
    cards = Card.query.filter_by(board_id=board_id)
    for card in cards:
        card_list.append(card.to_json())

    return {"board_id": board_id,
            "title": board.title,
            "cards": card_list, 
            'owner': board.owner,
            "color": board.color}, 200


@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    print(request_body)
    try:
        new_board = Board.create(request_body)
    except KeyError:
        return abort(make_response(jsonify({"details":"Invalid data"}), 400))

    # if not request_body.get("title") or not request_body.get("owner"):
    #     return {"details": "Invalid data"}, 400

    db.session.add(new_board)
    db.session.commit()

    return {"board": new_board.to_json()}, 201


@boards_bp.route("/<board_id>/cards", methods=["POST"])
def post_card_id_to_board(board_id):
    board = validate_record(Board, board_id)
    request_body = request.get_json()
    card=Card.create(request_body, board_id)
    db.session.add(card)
    db.session.commit()
    return jsonify({"board_id": board.board_id, "card_id": card.card_id, 'message': card.message, 'likes_count': card.likes_count}), 200