from flask import Blueprint, request, jsonify, make_response, abort
from sqlalchemy import func
from app import db
from app.models.board import Board

board_bp = Blueprint("board_bp", __name__, url_prefix="/boards")

#validation board helper function
def validate_board(board_id):
    board_id=int(board_id)
    boards = Board.query.all()
    for board in boards:
        if board_id==boards.board_id:
            return board
    abort(make_response({'details': 'This Board does not exist'}, 404))

# GET /boards
@board_bp.route("", methods=["GET"])
def get_all_boards():

    params = request.args
    if not params:
        boards = Board.query.all()
    elif "title" in params:
        found_title = params["title"]
        boards = Board.query.filter(func.lower(Board.title)==func.lower(found_title))
    elif "owner" in params:
        found_owner = params["owner"]
        boards = Board.query.filter(func.lower(Board.owner)==func.lower(found_owner))
    else: 
        return {"msg": "Sorry query not found, please search elsewhere."}

    board_reply = []
    for board in boards:
        board_reply.append({"title": board.title,
                            "owner": board.owner,
                            "id": board.board_id})
    return jsonify(board_reply)

# POST /boards
@board_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    new_board = Board(title=request_body["title"],
                    owner=request_body["owner"])

    db.session.add(new_board)
    db.session.commit()

    return make_response(f"New board: '{new_board.title}' succesfully created.  YAY!", 201)
