from flask import Blueprint, request, jsonify, make_response
from app import db


boards_bp = Blueprint('boards', __name__, url_prefix="/boards")


#READ all boards
@boards_bp.route("",methods=["GET"])
def read_all_boards():
    pass


#CREATE a new board
@boards_bp.route("", methods=["POST"])
def create_new_board():
    pass

#READ all cards belonging to a board
@boards_bp.route("/<board_id>/cards",methods=["GET"])
def read_all_cards(board_id):
    pass

#CREATE a new card for the selected board 
@boards_bp.route("/<board_id>/cards", methods=["POST"])
def create_new_card(board_id):
    pass
