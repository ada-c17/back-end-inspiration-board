from flask import Blueprint, request, jsonify, make_response, abort
from app import db
import requests
import sqlalchemy
from app import db
from app.models.board import Board
import sqlalchemy



board_bp = Blueprint("board_bp", __name__, url_prefix="/boards")

def validate_id(board_id):
    try:
        board_id = int(board_id)
    except ValueError:
        rsp = {"msg": f"Invalid id: {board_id}"}
        abort(make_response(jsonify(rsp), 400))
    chosen_board = Board.query.get(board_id)

    if chosen_board is None:
        rsp = {"msg": f"Could not find task with id {board_id}"}
        abort(make_response(jsonify(rsp), 404))
    return chosen_board


@board_bp.route("", methods=["POST"])
def create_new_task():
    request_body = request.get_json()

    try:
        title = request_body["title"]
        owner = request_body["owner"]
    except KeyError:
        return {"details": "Invalid data"}, 400

    new_board = Board(
        title=request_body["title"],
        owner=request_body["owner"],
    )
    
    db.session.add(new_board)
    db.session.commit()
    
    response = {"board": new_board.to_dict()}
    return jsonify(response), 201


@board_bp.route("", methods=["GET"])
def get_all_boards():
    response = []
    boards = Board.query.all()
    for board in boards:
        response.append(
            board.to_dict()
        )
    return jsonify(response)


@board_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    
    board = validate_id(board_id)
    return jsonify(board.to_dict()), 200


