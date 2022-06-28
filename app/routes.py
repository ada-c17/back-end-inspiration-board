from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from .models.board import Board
from .models.card import Card
from app.models import board

boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")
cards_bp = Blueprint("card_bp", __name__, url_prefix="/cards")

# ***** POST /boards *****
@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()

    if not "title"  in request_body or not "owner" in request_body:
        return jsonify({
            "details": "Must include title and owner"
        }), 400

    new_board = Board(title=request_body["title"], owner=request_body["owner"])

    db.session.add(new_board)
    db.session.commit()

    return {
        "title": new_board.title,
        "owner": new_board.owner
    }, 201

# ***** GET /boards *****
# validate id helper function
def validate_board(board_id):
    try:
        board_id = int(board_id)
    except ValueError:
        rsp = {"details": f"Invalid id: {board_id}"}
        abort(make_response(jsonify(rsp), 400))

    selected_board = Board.query.get(board_id)
    if selected_board is None:
        rsp = {"details": f"Could not find board with ID: {board_id}"}    
        abort(make_response(jsonify(rsp), 404))

    return selected_board    

@boards_bp.route('', methods=['GET'])
def get_all_boards():
    # sort_boards = request.args.get("sort")

    boards = Board.query.all()
    boards_response = [] 

    for board in boards:
        boards_response.append({
            "id": board.board_id,
            "title": board.title,
            "owner": board.owner,
        })

    return jsonify(boards_response), 200    

# @boards_bp.route("/<board_id>", methods=[GET])    

# ***** POST /boards/<board_id>/cards *****


# ***** GET /boards/<board_id>/cards *****


# ***** DELETE /cards/<card_id> *****


# ***** PUT /cards/<card_id>/like *****