import re
from flask import Blueprint, request, jsonify, make_response, abort
from sqlalchemy import func
from app import db
from app.models.board import Board
from .card_routes import Card, validate_card

board_bp = Blueprint("board_bp", __name__, url_prefix="/boards")

#Tori changed boards.board_id to board.board_id in line 15 below.
#validation board helper function
def validate_board(board_id):
    board_id=int(board_id)
    boards = Board.query.all()
    for board in boards:
        if board_id==board.board_id:
            return board
    abort(make_response({'details': 'This Board does not exist'}, 404))

# GET /boards
@board_bp.route("", methods=["GET"])
def get_all_boards():

    params = request.args
    if not params:
        boards = Board.query.all()
    elif "title" in params:
        found_title = params["title"]
        boards = Board.query.filter(func.lower(Board.title)==func.lower(found_title))
    elif "owner" in params:
        found_owner = params["owner"]
        boards = Board.query.filter(func.lower(Board.owner)==func.lower(found_owner))
    else: 
        return {"msg": "Sorry query not found, please search elsewhere."}

    board_reply = []
    for board in boards:
        board_reply.append({"title": board.title,
                            "owner": board.owner,
                            "id": board.board_id})
    return jsonify(board_reply)

# POST /boards
@board_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    new_board = Board(title=request_body["title"],
                    owner=request_body["owner"])

    db.session.add(new_board)
    db.session.commit()

    return make_response(f"New board: '{new_board.title}' succesfully created.  YAY!", 201)


# POST /boards/<board_id>/cards
@board_bp.route('/<board_id>/cards', methods=['POST'])
def post_cards_to_specific_board(board_id):
    board = validate_board(board_id)

    request_body = request.get_json()

    new_card = Card(message=request_body['message'])

    db.session.add(new_card)
    board.cards.append(new_card)
    db.session.commit()

    return jsonify({
        'card_id': new_card.card_id,
        'message': new_card.message,
        'board_id': board.board_id,
        'board_title': board.title
    }), 201


# GET /boards/<board_id>/cards
@board_bp.route('/<board_id>/cards', methods=['GET'])
def get_all_cards_for_specific_board(board_id):
    board = validate_board(board_id)
    card_list = []

    for card in board.cards:
        card_list.append(card.to_dict())

    return jsonify({
        'board_id': board.board_id,
        'board_title': board.title,
        'cards': card_list
    }), 200


# DELETE /boards/<board_id>
@board_bp.route('/<board_id>', methods=['DELETE'])
def delete_board(board_id):
    board = validate_board(board_id)

    db.session.delete(board)
    db.session.commit()

    return{'details': f'Board {board_id} was successfully deleted'}, 200


@board_bp.route ('/<board_id>', methods=['PUT'])
def patch_board_title(board_id):
    board = validate_board(board_id)
    request_body = request.get_json()
    try: 
        board.title = request_body['title']
        board.owner = request_body['owner']
    except KeyError:
        return jsonify({"details": "Please enter both Title and Owner"}), 400
    db.session.commit()

    return ({'Board': board.to_dict()}), 200




