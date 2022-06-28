from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards_bp", __name__, url_prefix="/tasks")

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