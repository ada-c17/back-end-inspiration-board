from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board


# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint('board_bp', __name__, url_prefix="/boards/")

@board_bp.route("<board_id>", strict_slashes=False)
def get_one_board(board_id):
    #validate board_id
    board = Board.query.get(board_id)
    return {
            "title": board.title,
            "owner": board.owner,
            "cards": [card.to_json() for card in board.cards]
            }
# board routes

# create board
@board_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    try:
        new_board = Board.from_json(request_body)

        db.session.add(new_board)
        db.session.commit()

    except:
        abort(make_response("Invalid data", 400))

    return make_response("Success", 201)


# get all boards
@board_bp.route("", methods=["GET"], strict_slashes=False)
def get_boards():
    # do sort stuff
    boards = Board.query.all()
    boards_response = [board.to_json() for board in boards]
    return jsonify(boards_response)