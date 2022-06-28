from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card


##### TABLE OF CONTENTS #############################################

#   [0] IMPORTS
#   [1] BLUEPRINT DEFINITIONS
#   [2] HELPER FUNCTIONS
#   [3] BOARD ENDPOINTS
#   [4] CARD ENDPOINTS


##### [1] BLUEPRINT DEFINITIONS #####################################

board_bp = Blueprint('board_bp', __name__, url_prefix='/boards')
card_bp = Blueprint('card_bp', __name__, url_prefix='/cards')


##### [2] HELPER FUNCTIONS ##########################################

def validate_id(object_id, object_type):
    '''
    Validates the board or card based on ID and fetches the object from the database.
        *object_id:  id of a board or card
        *object_type: "board" or "card" depending on endpoint
        OUTPUT: board or card object fetched from database.
    '''
    try:
        object_id = int(object_id)
    except:
        abort(make_response({"message":f"{object_type} {object_id} invalid"}, 400))

    if object_type == "board":
        response = Board.query.get(object_id)
    elif object_type == "card":
        response = Card.query.get(object_id)
    if not response:
        abort(make_response({"message":f"{object_type} {object_id} not found"}, 404))

    return response


##### [3] BOARD ENDPOINTS ###########################################

@board_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()
    return jsonify([board.to_dict() for board in boards]), 200


@board_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    board = validate_id(board_id, "board")
    return jsonify(board.to_dict()), 200


@board_bp.route("", methods=["POST"])
def post_board():
    request_body = request.get_json()

    if "title" in request_body and "owner" in request_body:
        new_board = Board(title=request_body["title"],
                    owner=request_body["owner"])
    else:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_board)
    db.session.commit()

    return make_response(new_board.to_dict(), 201)



##### [4] CARD ENDPOINTS ############################################

@card_bp.route("", methods=["GET"])
def get_all_cards():
    cards = Card.query.all()
    return jsonify([card.to_dict() for card in cards]), 200


@card_bp.route("/<card_id>", methods=["GET"])
def get_one_card(card_id):
    card = validate_id(card_id, "card")
    return jsonify(card.to_dict()), 200


@card_bp.route("", methods=["POST"])
def post_card():
    request_body = request.get_json()

    if "message" in request_body and "board_id" in request_body:
        if len(request_body["message"]) > 40:
            abort(make_response({"details": "Messages cannot be longer than 40 characters"}, 400))
        new_card = Card(
            message=request_body["message"],
            likes_count=0,
            board_id=request_body["board_id"],
            )
    else:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_card)
    db.session.commit()

    return make_response(new_card.to_dict(), 201)


@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_one_card(card_id):
    card = validate_id(card_id, "card")
    db.session.delete(card)
    db.session.commit()
    return {"message" : f'Card {card_id} successfully deleted'}, 200


@card_bp.route("/<card_id>/like", methods=["PATCH"])
def update_card_likes(card_id):
    card = validate_id(card_id, "card")
    card.likes_count += 1
    db.session.commit()
    return jsonify({'msg': f'updated like count for card with id {card_id}. Likes now at {card.likes_count}'}), 200

