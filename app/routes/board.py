from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.routes.helper import validate

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()

    new_board = Board(
        title=request_body["title"],
        owner=request_body["owner"]
    )

    db.session.add(new_board)
    db.session.commit()

    return {
        "id": new_board.board_id
    }, 201

@boards_bp.route("", methods=["GET"])
def get_all_boards():
    response = []
    boards = Board.query.order_by(Board.board_id).all()
    for board in boards:
        response.append(
            {
                "id": board.board_id,
                "title": board.title,
                "owner": board.owner
            }
        )
    return jsonify(response)

@boards_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    board = validate(Board, board_id)
    response = {
                "id": board.board_id,
                "title": board.title,
                "owner": board.owner
            }
    return jsonify(response)

@boards_bp.route("/<board_id>", methods=["PUT"])
def update_board(board_id):
    board = validate(Board, board_id)
    request_body = request.get_json()

    if "title" not in request_body:
        return jsonify({'msg': f"Request must include title"}), 400

    board.title = request_body["title"]

    db.session.commit()

    return make_response(
        jsonify({'msg': f"Successfully updated board {board_id}"}), 200
    )

@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = validate(Board, board_id)
    db.session.delete(board)
    db.session.commit()

    response = {'details': f'Board {board_id} "{board.title}" successfully deleted'}

    return make_response(jsonify(response), 200)

    

