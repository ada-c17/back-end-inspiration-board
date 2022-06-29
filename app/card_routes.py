from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from app.models.board import Board

# example_bp = Blueprint('example_bp', __name__)
card_bp = Blueprint('card_bp', __name__, url_prefix="/boards/")
board_bp = Blueprint('board_bp', __name__, url_prefix="/boards/")
@card_bp.route("<board_id>/cards", methods=["CREATE"], strict_slashes=False)
def create_card(board_id):
    #validate
    request_body = request.get_json()
    new_card = Card(message=request_body["message"], board_id=board_id)

    db.session.add(new_card)
    db.session.commit()

    return make_response("Success", 201)

@card_bp.route("<board_id>/cards/<card_id>", methods=["PATCH"], strict_slashes=False)
def update_card(board_id, card_id):
    #validate board_id
    #validate card_id
    card = Card.query.get(card_id)

    request_body = request.get_json()
    card["message"] = request_body["message"]

    db.session.commit()
    return make_response("Success", 200)

# delete single card
@card_bp.route("<board_id>/cards/<card_id>", methods=["DELETE"], strict_slashes=False)
def delete_card(board_id, card_id):
    # add helper function to validate board_id
    # add helper function to validate card_id
    
    card = Card.query.get(card_id)

    db.session.delete(card)
    db.session.commit()
    return make_response("Card successfully deleted", 200)

# board routes

# get all boards
@board_bp.route("", methods=["GET"], strict_slashes=False)
def get_boards():
    # do sort stuff
    boards = Board.query.all()
    boards_response = [board.to_json() for board in boards]
    return jsonify(boards_response)