from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")


#get all elements 
@boards_bp.route("", methods = ["GET"])
def get_all_boards():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        boards = Board.query.order_by(asc(Task.title))
    elif sort_query == "desc":
        boards = Board.query.order_by(desc(Task.title))
    else:
        boards = Board.query.all()
    return jsonify([board.to_dict_board() for board in boards]), 200


#get one board using Get in routes and accessing by id
@boards_bp.routes("/<board_id>", methods= ["GET"])
def get_one_board(board_id):
    board = validate_board(board_id)
    if board.card_id:
        response = {"board":{
            "id": board.board_id,
            "card_id": board.card_id,
            "title": board.title,
            "owner": board.owner
        }
    }
    else:
        response = {"board":board.to_dict_board()}
    return jsonify(response), 200
