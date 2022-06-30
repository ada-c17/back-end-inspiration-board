from flask import Blueprint, request, jsonify, make_response, abort
from sqlalchemy import func
from app import db
from app.models.board import Board
from .card_routes import Card

board_bp = Blueprint('board_bp', __name__, url_prefix='/boards')


#validation of board helper function
def validate_board(board_id):
    try:
        board_id=int(board_id)
    except:
        abort(make_response({'details': f'Board {board_id} invalid'}, 400))

    board = Board.query.get(board_id)
    
    if not board:
        abort(make_response({'details': f'Board {board_id} does not exist'}, 404))


# GET all boards
@board_bp.route('', methods=['GET'])
def get_all_boards():

    params = request.args
    if not params:
        boards = Board.query.all()
    elif 'title' in params:
        found_title = params['title']
        boards = Board.query.filter(func.lower(Board.title)==func.lower(found_title))
    elif 'owner' in params:
        found_owner = params['owner']
        boards = Board.query.filter(func.lower(Board.owner)==func.lower(found_owner))
    else: 
        return {'details': 'Sorry query not found, please search elsewhere.'}

    wall = []
    for board in boards:
        wall.append({'title': board.title,
                            'owner': board.owner,
                            'id': board.board_id})
    return jsonify(wall)


# # GET all boards
# @board_bp.route('', methods=['GET'])
# def get_all_boards():
#     boards = Board.query.all()

#     wall = []
#     for board in boards:
#         wall.append(board.to_dict())

#     return jsonify(wall), 200


# GET one board by id
@board_bp.route ('/<board_id>', methods=['GET'])
def get_one_board (board_id):
    board = validate_board(board_id)
    return ({'Board': board.to_dict()}), 200


#POST a new Board
@board_bp.route('', methods=['POST'])
def create_board():
    request_body = request.get_json()
    new_board = Board(title=request_body['title'],
                    owner=request_body['owner'])

    db.session.add(new_board)
    db.session.commit()

    return make_response(f'New board: "{new_board.title}" succesfully created.  YAY!', 201)


# POST a new Card for a specific Board
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


# GET get ALL cards from ONE Board
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


# DELETE ONE Board
@board_bp.route('/<board_id>', methods=['DELETE'])
def delete_board(board_id):
    board = validate_board(board_id)

    db.session.delete(board)
    db.session.commit()

    return{'details': f'Board {board_id} was successfully deleted'}, 200


# UPDATE attributes of Board
@board_bp.route ('/<board_id>', methods=['PUT'])
def put_board_title(board_id):
    board = validate_board(board_id)

    request_body = request.get_json()
    
    try: 
        board.title = request_body['title']
        board.owner = request_body['owner']
    
    except KeyError:
        return jsonify({'details': 'Please enter both Title and Owner'}), 400
    
    db.session.commit()

    return ({'Board': board.to_dict()}), 200




