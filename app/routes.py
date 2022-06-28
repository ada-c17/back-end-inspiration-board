from crypt import methods
from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
# example_bp = Blueprint('example_bp', __name__)

boards_bp = Blueprint("boards", __name__, url_prefix="/boards") 

# Get board
@boards_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()
    boards_response = [board.to_dict() for board in boards]

    return jsonify(boards_response), 200

# Create board
@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()

    try:
        new_board = Board.create(request_body)
    except KeyError:
        return make_response({"details":"Invalid data"}, 400)

    db.session.add(new_board)
    db.session.commit()

    return jsonify({"board":new_board.to_dict()}), 201


# Delete board
@boards_bp.route("/<id>", methods=["DELETE"])
def delete_board(id):
    def validate_board(id):
        board = Board.query.get(id)

        if not board:
            abort(make_response({"message": f"board {id} not found"}, 404))

        return board
    board = validate_board(id)

    db.session.delete(board)
    db.session.commit()

    return jsonify({"details": f'board id:{id}, title:{board.title}, owner:{board.owner} successfully deleted'}), 200
