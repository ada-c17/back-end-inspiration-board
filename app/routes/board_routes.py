from flask import Blueprint, request, jsonify, make_response
from app import db

from app.models.board import Board
# from .routes import validate_card

from datetime import datetime
# example_bp = Blueprint('example_bp', __name__)

boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

# CREATE aka POST new board at endpoint: /boards
@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response(jsonify(dict(details="Invalid data")), 400)
    
    new_board = Board.create(request_body)
    
    db.session.add(new_board)
    db.session.commit()

    return make_response(jsonify({"board": new_board.to_dict()}), 201)   

#######

#app/board_routes.py
@boards_bp.route("/<board_id>/cards", methods=["POST"])
def create_card_for_board(board_id):
    board = validate_board(board_id)
    request_body = request.get_json()
    
    cards_list = []

    for card_id in request_body["card_ids"]:
        card = validate_card(card_id)
        card.board = board 
        cards_list.append(card.card_id)

    db.session.commit()

    return make_response(jsonify(dict(id=board.board_id, card_ids=cards_list))), 200
    # return make_response(jsonify(f"id: {card.title} for Board: {card.board.title} successfully created"), 200)

@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_cards_per_board(board_id):

    board = validate_board(board_id)
    cards_info = [card.to_dict() for card in board.cards]

    db.session.commit()

    return jsonify(dict(id=board.board_id, title=board.title, cards=cards_info)), 200


# GET ALL boardS aka READ at endpoint /boards
@boards_bp.route("", methods=["GET"])
def read_all_boards():
    boards_response = []

    title_query = request.args.get("sort")

    if title_query == "asc":
        boards = Board.query.order_by(Board.title.asc())

    elif title_query == "desc":
        boards = Board.query.order_by(Board.title.desc())
    
    else:
        boards = Board.query.all()

    boards_response = [board.to_dict() for board in boards]

    return make_response(jsonify(boards_response), 200) 

#####
# GET aka READ board at endpoint: /boards/id 
@boards_bp.route("/<id>", methods=["GET"])
def get_board_by_id(id):
    board = validate_board(id)

    # NOTE: Flask will automatically convert a dictionary into an HTTP response body. 
    # If we don't want to remember this exception, we can call jsonify() with the dictionary as an argument to return the result
    return jsonify({"board": board.to_dict()}), 200
    # return make_response(jsonify({"board": board.to_dict()}), 201)

# *************Could alternatively use a hash to look things up by id.  ...need to practice this later. 

@boards_bp.route("/<id>", methods=['PUT'])
def update_board(id):
    board = validate_board(id)

    request_body = request.get_json()

    board.update(request_body)
    db.session.commit()
    return jsonify({"board": board.to_dict()}), 200
    
# DELETE /boards/id
@boards_bp.route("<id>", methods=['DELETE'])
def delete_one_board(id):
    board = validate_board(id)

    db.session.delete(board)
    db.session.commit()

    return jsonify({'details': f'Board {id} "{board.title}" successfully deleted'}), 200

#QUALITY CONTROL HELPER FUNCTION
def validate_board(id):
    try:
        id = int(id)
    except ValueError: 
        # return jsonify({}), 400     .....OR
        abort(make_response(jsonify(dict(details=f"invalid id: {id}")), 400))

    board = Board.query.get(id)
    if board:
        return board

    elif not board:
        abort(make_response(jsonify("board not found"), 404))

    
#########   
# PATCH a board at endpoint: boards/id  #Remember PATCH is just altering one or some attributes whereas PUT replaces a record. 
@boards_bp.route("/<id>", methods=["PATCH"])
def update_one_board(id):
    board = validate_board(id)
    request_body = request.get_json()
    board_keys = request_body.keys()

    if "title" in board_keys:
        board.title = request_body["title"]

    db.session.commit()
    return make_response(f"Board# {board.board_id} successfully updated"), 200

# PATCH a board at endpoint: boards/id/mark_complete 
@boards_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_complete(id):
    board = validate_board(id)
    
    # if board.completed_at:
    board.completed_at = datetime.utcnow()

    db.session.commit()

    return make_response(jsonify({"board": board.to_dict()}), 200)

# PATCH a board at endpoint: boards/id/mark_incomplete
@boards_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(id):
    board = validate_board(id)

    board.completed_at = None

    db.session.commit()
    return make_response(jsonify({"board": board.to_dict()}), 200)





