from flask import Blueprint, request, jsonify
from app import db
from app.models.board import Board
from app.helper import get_board_or_abort


boards_bp = Blueprint('boards_bp', __name__, url_prefix="/boards")


@boards_bp.route("", methods=['POST'])
def create_one_board():
    request_body = request.get_json()

    try:
        new_board = Board(title = request_body["title"],owner = request_body["owner"])
    except KeyError:
        return { "details": "Invalid data"}, 400
    db.session.add(new_board)
    db.session.commit()
    return jsonify(
        {
            "board": new_board.to_dict()
        }
    ),201


@boards_bp.route("", methods=['GET'])
def get_all_boards():
    boards = Board.query.all()
    boards_response = []
    for board in boards:
        boards_response.append(board.to_dict())

    return jsonify(boards_response), 200


# GET /boards
@boards_bp.route('/<board_id>', methods=['GET'])
def get_one_board(board_id):
    board = get_board_or_abort(board_id)
    # return jsonify(board.to_dict()), 200
    return jsonify(
        {
            "board": board.to_dict()
        }
    ), 200

# DELETE /boards/<board_id>
@boards_bp.route('/<board_id>', methods=['DELETE'])
def delete_one_board(board_id):
    board = get_board_or_abort(board_id)
    db.session.delete(board)
    db.session.commit()

    return {
        "details": f'Board {board.board_id} "{board.title}" successfully deleted'
    }, 200
