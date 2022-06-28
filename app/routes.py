from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board 


boards_bp = Blueprint('boards_bp', __name__, url_prefix='/boards')

@boards_bp.route('', methods=['GET'])
def list_all_boards():
    board_query = request.args.get("sort")
    boards = Board.query.all()
    board_response = []
    for board in boards:
        board_response.append(
            {
                "id":board.board_id,
                "title":board.title,
                "owner":board.owner,
            }
        )
    return jsonify(board_response)