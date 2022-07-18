from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card

boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

#VALIDATING IDS FOR BOARDS AND CARDS
def validate_board_id(board_id):
    try:
        board_id =  int(board_id)
    except:
        return abort(make_response(jsonify({'message': f"Invalid board {board_id}"}), 400))
    board = Board.query.get(board_id)

    if board is None:
        return abort(make_response(jsonify({'message': f"board {board_id} not found"}), 404))
    return board

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


#CREATE ONE NEW BOARD
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

#READ (GET) ONE BOARD
@boards_bp.route('<board_id>', methods=["GET"])
def get_one_board(board_id):
    one_board = validate_board_id(board_id)
    response = {
            "id": one_board.board_id,
            "title": one_board.title,
            "owner": one_board.owner
        }
    return jsonify({"board": response}), 200

#READ (GET) ALL BOARD
@boards_bp.route('', methods=['GET'])
def read_all_boards():
    boards = Board.query.all()
    boards_response = []

    for board in boards:
        boards_response.append({
            "id": board.board_id,
            "title": board.title,
            "owner": board.owner
        })
    
    return jsonify(boards_response), 200

#UPDATE ONE BOARD
@boards_bp.route("/<board_id>", methods=["PUT"])
def update_board(board_id):
    board = validate_board_id(board_id)
    request_body = request.get_json()

    board.title = request_body["title"]

    db.session.commit()
    return jsonify({
        "board": {
            "id": board.board_id,
            "title": board.title,
            "owner": board.owner
        }
    }), 200

#CREATE ONE CARD AT BOARD ID
@boards_bp.route('/<id>/cards', methods=['POST'])
def create_one_card(id):
    request_body = request.get_json()
    
    if 'message' not in request_body:
        return {"message": "Please add a message to post a card"}, 400

    new_card = Card(message = request_body['message'],
                    color=request_body['color'],
                    PosX=100,
                    PosY=0,
                    likes_count=0,
                    board_id = id)
    
    db.session.add(new_card)
    db.session.commit()
    return {
        "card": {
        "id": new_card.card_id,
        "PosX": new_card.PosX,
        "PosY": new_card.PosY,
        "message": new_card.message,
        "color": new_card.color,
        "likes_count": new_card.likes_count
    }}, 201



#Delete board
@boards_bp.route('/<board_id>', methods = ['DELETE'])
def delete_board(board_id):
    chosen_board = validate_board_id(board_id)
    db.session.delete(chosen_board)
    db.session.commit()

    return {
        'details':f'board {chosen_board.board_id} {chosen_board.title} successfully deleted'
    }, 200

#Delete card
@cards_bp.route('/<card_id>', methods = ['DELETE'])
def delete_card(card_id):
    chosen_card = get_card_or_abort(card_id)
    db.session.delete(chosen_card)
    db.session.commit()

    return {
        'details':f'card {chosen_card.card_id} {chosen_card.message} successfully deleted'
    }, 200

#READ ALL CARDS FOR ONE BOARD
@boards_bp.route('/<board_id>/cards', methods=['GET'])
def read_cards_of_one_board(board_id):

    board = validate_board_id(board_id)

    cards_response = []

    for card in board.cards:
            cards_response.append(
                {
                    "id": card.card_id,
                    "board_id": board.board_id,
                    "message": card.message,
                    "PosX": card.PosX,
                    "PosY": card.PosY,
                    "color": card.color,
                    "likes_count": card.likes_count
                }    
        )
            
    return jsonify({
            'id': board.board_id,
            'title': board.title,
            'owner': board.owner,
            'cards': cards_response}), 200

#UPDATE LIKE COUNT 
@cards_bp.route('/<card_id>/like', methods=['PUT'])
def update_one_card_like_count(card_id):
    card = get_card_or_abort(card_id)
    
    card.likes_count += 1

    db.session.commit()

    return { 'card': {
        'id': card.card_id,
        'message': card.message,
        'PosX': card.PosX,
        'PosY': card.PosY,
        'color': card.color,
        'likes_count': card.likes_count
        }}, 200


#UPDATE ONE CARD
@cards_bp.route('/<card_id>', methods=['PUT'])
def update_card(card_id):
    card = get_card_or_abort(card_id)
    request_body = request.get_json()

    card.PosX= request_body["PosX"]
    card.PosY= request_body["PosY"]

    db.session.commit()
    return {
        "card": {
        "id": card.card_id,
        "message": card.message,
        "PosX": card.PosX,
        "PosY": card.PosY,
        "color": card.color,
        "likes_count": card.likes_count
    }}, 200

