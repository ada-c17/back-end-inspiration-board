from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")
@boards_bp.route("", methods=["GET"])
def get_all_boards():
    
    boards = Board.query.all()
    board_response = []
    board_response = [board.to_json() for board in boards]
    return jsonify(board_response), 200


def validate_board(cls, id):
    try:
        board_id = int(id)
    except:
        abort(make_response({"details": "Invalid data"}, 400))
    obj = cls.query.get(id)
    if not obj:
        abort(make_response({"message": f"{cls.__name__} not found"}, 404))
        
    return obj
@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_cards_by_board(board_id):
    board_id = int(board_id)
    board = validate_board(board_id)
    card_list = []
    cards = Card.query.filter_by(board_id=board_id)
    for card in cards:
        card_list.append(card.to_json())

    return {"id": board_id,
            "title": board.title,
            "cards": card_list, 
            'owner': board.owner}, 200


@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    if not request_body.get("title") or not request_body.get("owner"):
        return {"details": "Invalid data"}, 400
    new_board = Board.create(request_body)

    db.session.add(new_board)
    db.session.commit()

    return {"board": new_board.to_json()}, 201
