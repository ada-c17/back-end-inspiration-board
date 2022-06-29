
from flask import Blueprint, jsonify, request, abort, make_response
from app.models.board import Board
from app import db

boards_bp = Blueprint('boards_bp', __name__, url_prefix='/boards')

def validate_board_id(board_id):
    try:
        board_id = int(board_id)
    except TypeError:
        abort(make_response({"details": "Board ID is invalid data type"}, 400
                            ))
    board = Board.query.get(board_id)
    if not board:
        abort(make_response({"details": f"No board with id: {board_id}"}, 404
                            ))
    return board
        

@boards_bp.route('', methods=['GET'])
def get_all_boards():
    boards = Board.query.all()

    response_body = [board.to_json() for board in boards]

    return jsonify(response_body), 200


@boards_bp.route('/<board_id>/cards', methods=['GET'])
def get_all_cards_from_board(board_id):
    board = validate_board_id(board_id)
    cards = board.cards
    list_all_cards = []
    for card in cards:
        list_all_cards.append({'id': card.card_id, 'message': card.message, 'likes_count': card.likes_count})
    
    return jsonify(list_all_cards), 200


@boards_bp.route('', methods=['POST'])
def post_new_board():
    new_board_request = request.get_json()
    try:
        new_board = Board(title=new_board_request['title'], owner=new_board_request['owner'])
    except KeyError:
        return {'error details': 'Title and Owner are required to create a board'}, 400
    db.session.add(new_board)
    db.session.commit()

    rsp = {'message': f'New board created with id: {new_board.board_id}'}
    return rsp, 201

