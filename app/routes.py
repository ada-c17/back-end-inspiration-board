from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

@boards_bp.route('', methods=['POST'])
def create_one_board():
    request_body = request.get_json()
    if 'title' not in request_body or 'owner' not in request_body:
        return {"message": "Please enter both title and owner"}, 400
    
    new_board = Board(title=request_body['title'], 
                    owner=request_body['owner'])
    db.session.add(new_board)
    db.session.commit()
    return {
        "board": {
        "id": new_board.board_id,
        "title": new_board.title,
        "owner": new_board.owner
    }}, 201








#Update
#updating a card to add +1

@cards_bp.route('/<card_id>', methods=['PUT'])
def replace_one_card(card_id):
    chosen_card = get_card_or_abort(card_id)
    request_body = request.get_json()

    try:
        chosen_card.message = request_body['message']
        chosen_card.likes_count = request_body['likes_count']
        
    except KeyError:
        return {
            'message': 'card 1 not found'
        } , 400

    db.session.commit()

    return { 'card': {
        'message': chosen_card.message,
        'likes_count': chosen_card.likes_count
        }}, 200

#Delete card
@cards_bp.route('/<card_id>', methods = ['DELETE'])
def delete_card(card_id):
    chosen_card = get_card_or_abort(card_id)
    db.session.delete(chosen_card)
    db.session.commit()

    return {{
        'details':f'card 1 \'{chosen_card.message}\' successfully deleted'
    }}, 200


#helper function for card 

def get_card_or_abort(card_id):
    try:
        card_id = int(card_id)
    except ValueError:
        response = {'details': 'Invalid data'}
        abort(make_response(jsonify(response),400))

    chosen_card = Card.query.get(card_id)

    if chosen_card is None:
        response = {'message':f'card {card_id} not found'}
        abort(make_response(jsonify(response),404))
    return chosen_card

#helper function for board
def get_board_or_abort(board_id):
    try:
        board_id = int(board_id)
    except ValueError:
        response = {'details': 'Invalid data'}
        abort(make_response(jsonify(response),400))

    chosen_board = Board.query.get(board_id)

    if chosen_board is None:
        response = {'message':f'board {board_id} not found'}
        abort(make_response(jsonify(response),404))
    return chosen_board



@boards_bp.route('/<board_id>/cards', methods=['GET'])
def read_cards_of_one_board(board_id):

    board = get_board_or_abort(board_id)

    cards_response = []

    for card in board.cards:
            cards_response.append(
                {
                    "id": card.card_id,
                    "board_id": board.board_id,
                    "message": card.message,
                    "likes_count": card.likes_count
                }    
        )
            
    return jsonify({
            'id': board.board_id,
            'title': board.title,
            'owner': board.owner,
            'cards': cards_response}), 200