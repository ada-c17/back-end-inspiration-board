from flask import Blueprint, request, jsonify, make_response, abort
from app.models.board import Board
from app import db
from sqlalchemy import asc, desc

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

def validate_request(request_body):
    if "title" not in request_body or "owner" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

# helper function for validate id
def get_board_or_abort(board_id):
    try:
        board_id = int(board_id)
    except ValueError:
        abort(make_response({"message": f"The board id {board_id} is invalid. The id must be integer."}, 400))

    board = Board.query.get(board_id)
    if not board:
        abort(make_response({"message": f"The board id {board_id} is not found"}, 404))

    return board

@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    validate_request(request_body)

    new_board = Board(
        title = request_body["title"],
        owner = request_body["owner"]
    )

    db.session.add(new_board)
    db.session.commit()
    return jsonify({"board": new_board.make_json()}), 201

# get all elements 
@boards_bp.route("", methods = ["GET"])
def get_all_boards():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        boards = Board.query.order_by(asc(Board.title))
    elif sort_query == "desc":
        boards = Board.query.order_by(desc(Board.title))
    else:
        boards = Board.query.all()
    return jsonify([board.make_json() for board in boards]), 200

#get one board using Get in routes and accessing by id
@boards_bp.route("/<board_id>", methods= ["GET"])
def get_one_board(board_id):
    board = get_board_or_abort(board_id)
    return jsonify({"board": board.make_json_with_cards()}), 200

@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_a_board(board_id):
    board = get_board_or_abort(board_id)

    db.session.delete(board)
    db.session.commit()

    return make_response({'details':f'Board {board.board_id} "{board.title}" successfully deleted'}, 200)
