from turtle import title
import requests
import os
from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.board import Card

# # example_bp = Blueprint('example_bp', __name__)

# # Boards Routes

#? Do we want to add a board & card validation function in here? 
#? Or can we assume the frontend passes only valid data?

# boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

# # POST /boards
# @boards_bp.route("", methods=["POST"])

def create_board():
    try:
        request_body = request.get_json()
        new_board = Board(
            title=request_body["title"], 
            owner=request_body["owner"]
            )
        
        if "cards" in request_body:
            new_board.cards = request_body["cards"]

        db.session.add(new_board)
        db.session.commit()

        #? I had something like the below in my task_list to return the board 
        #? data on successful post. It needs a single_dict method in the Board class.

        # return make_response(jsonify(new_board.single_dict()), 201)
        return make_response(jsonify({"board created!":new_board.title}), 201)

    except KeyError:
        return make_response(jsonify({"details":"Invalid data"}), 400)

# # GET /boards/<board_id>
# @boards_bp.route("/<board_id>", methods=["GET"])
def read_all_boards():
    boards = Board.query.all()

    boards_response = []
    for board in boards:
        boards_response.append(board.to_dict())
    
    return make_response(jsonify(boards_response), 200)

# # PUT /boards/<board_id> ??? Do we want ???
# @boards_bp.route("/<board_id>", methods=["PUT"])

# # ??? Do we want PATCH routes for title or owner ???

# # DELETE /boards/<board_id>
# @boards_bp.route("/<board_id>", methods=["DELETE"])

# # Cards Routes

# cards_bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

# # POST /cards
# @cards_bp.route("", methods=["POST"])

# # GET /cards
# @cards_bp.route("", methods=["GET"])

# # PUT /cards/<card_id>/ ??? Do we want ???

# # PATCH /cards/<card_id>/likes_count
# @cards_bp.route("/<card_id>/likes_count", methods=["PATCH"])

# # ??? Do we want PATCH route for message ???

# # DELETE /cards/<card_id>
# @cards_bp.route("/<card_id>", methods=["DELETE"])
