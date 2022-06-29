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
        return abort(make_response(jsonify({'message': f"Invalid task: {board_id}"}), 400))
    board = Board.query.get(board_id)

    if board is None:
        return abort(make_response(jsonify({'message': f"board {board_id} not found"}), 404))
    return board


#Creating one new board using POST method
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