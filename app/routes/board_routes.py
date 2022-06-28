from flask import Blueprint, request, jsonify, make_response
from app import db


boards_bp = Blueprint('boards', __name__, url_prefix="/boards")


#READ all boards
@boards_bp.route("",methods=["GET"])
def read_all_boards():
    pass

#READ a specific board
@boards_bp.route("/<board_id>", methods=["GET"])
def read_one_board(board_id):
    pass

#CREATE a new board
@boards_bp.route("", method=["POST"])
def create_new_board():
    pass

#READ all cards belonging to a board
@boards_bp.route("/<board_id>/cards",methods=["GET"])
def read_all_cards(board_id):
    pass
