from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.card import Card

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint('board_bp', __name__, url_prefix='/boards')
card_bp = Blueprint('card_bp', __name__, url_prefix='/cards')

#create a new board using "title" and "owner" inputs

    #see error message if title or owner is blank/empty/invalid/missing

#read: view list of all boards; select a board
# @board_bp.route("", methods=["GET"])
# def get_all_boards():
#     boards = Board.query.all()

#     boards_response = []
#     for board in boards:
#         boards_response.append(board.to_dict())
    
#     return jsonify(boards_response)