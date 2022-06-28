from flask import Blueprint, request, jsonify, make_response, abort
from app.models.board import Board
from app import db
from sqlalchemy import asc, desc




# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    if "title" not in request_body or "owner" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_board = Board(
        title = request_body["title"],
        owner = request_body["owner"]
    )

    db.session.add(new_board)
    db.session.commit()
    return jsonify({"board": new_board.to_dict_board()}), 201

#get all elements 
@boards_bp.route("", methods = ["GET"])
def get_all_boards():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        boards = Board.query.order_by(asc(Board.title))
    elif sort_query == "desc":
        boards = Board.query.order_by(desc(Board.title))
    else:
        boards = Board.query.all()
    return jsonify([board.to_dict_board() for board in boards]), 200


#get one board using Get in routes and accessing by id
@boards_bp.route("/<board_id>", methods= ["GET"])
def get_one_board(board_id):
    board = Board.query.get(id)
    board = get_board_or_abort(board_id)
    if board.card_id:
        response = {"board":{
            "id": board.board_id,
            "cards": board.card_id,
            "title": board.title,
            "owner": board.owner
        }
    }
    else:
    response = {"board":board.to_dict_board()}
    return jsonify(response), 200


def get_board_or_abort(board_id):
    try:
        board_id = int(board_id)
    except ValueError:
        abort(make_response({"message": f"The task id {board_id} is invalid. The id must be integer."}, 400))
    
    boards = Board.query.all()
    for board in boards:
        if board.board_id == board_id:
            return board
    abort(make_response({"message": f"The task id {board_id} is not found"}, 404))





