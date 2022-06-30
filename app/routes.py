from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

def validate_board_id(board_id):
    try:
        board_id =  int(board_id)
    except:
        return abort(make_response(jsonify({'message': f"Invalid board {board_id}"}), 400))
    board = Board.query.get(board_id)

    if board is None:
        return abort(make_response(jsonify({'message': f"board {board_id} not found"}), 404))
    return board

#FROM DOINA'S BRANCH
# def validate_board(board_id):
#     board = Board.query.get(board_id)

#     if board is None:
#         abort(make_response(jsonify(f"Board {board_id} not found"), 404))

#     return board


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

@boards_bp.route('<board_id>', methods=["GET"])
def get_one_board(board_id):
    one_board = validate_board_id(board_id)
    response = {
            "id": one_board.board_id,
            "title": one_board.title,
            "owner": one_board.owner
        }
    return jsonify({"board": response}), 200

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
    
    return jsonify(boards_response)


@boards_bp.route("/<board_id>", methods=["PUT"])
def update_board(board_id):
    board = validate_board_id(board_id)
    request_body = request.get_json()

    board.title = request_body["title"]
    board.owner = request_body["owner"]

    db.session.commit()
    return jsonify({
        "board": {
            "id": board.board_id,
            "title": board.title,
            "owner": board.owner
        }
    }), 200

@boards_bp.route('/<id>/cards', methods=['POST'])
def create_one_card(id):
    request_body = request.get_json()
    
    if 'message' not in request_body:
        return {"message": "Please enter both message and likes"}, 400

    new_card = Card(message = request_body['message'],
                    board_id = id)
    
    db.session.add(new_card)
    db.session.commit()
    return {
        "card": {
        "id": new_card.card_id,
        "message": new_card.message,
        "likes_count": new_card.likes_count
    }}, 201



    



