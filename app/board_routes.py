import re
from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board

board_bp = Blueprint('boards', __name__, url_prefix="/boards")


@board_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()

    if "owner" not in request_body or str(request_body["owner"]).split() == []:
        return jsonify(
            {
                "details": "Please provide owner information!"
            }), 400
    if "title" not in request_body or str(request_body["title"]).split() == []:
        return jsonify(
            {
                "details": "Please provide title!"
            }), 400
    elif len(str((request_body["title"]))) > 40 or len(str((request_body["owner"]))) > 40:
        return jsonify(
            {
                "details": "Please enter a message that is less than 40 characters!"
            }), 400
    else:
        new_board = Board(
            title=request_body["title"], owner=request_body["owner"])

    db.session.add(new_board)
    db.session.commit()

    return make_response(jsonify(f"Board {new_board.title} with id {new_board.board_id} succesfully created"), 201)


@board_bp.route("", methods=["GET"])
def read_all_boards():

    boards = Board.query.all()

    boards_response = []
    for board in boards:
        boards_response.append(
            {
                "board_id": board.board_id,
                "title": board.title,
                "owner": board.owner
            }
        )
    return jsonify(boards_response)


def validate_board(board_id):
    try:
        board_id = int(board_id)
    except:
        abort(make_response({"message": f"board id {board_id} invalid"}, 400))

    board = Board.query.get(board_id)

    if not board:
        abort(make_response(
            {"message": f"board with {board_id} not found"}, 404))

    return board


# @board_bp.route("/<board_id>", methods=["GET"])
# def read_one_board_with_all_cards(board_id):

#     board = validate_board(board_id)
#     cards = []
#     for card in board.cards:
#         cards.append({
#             "card_id": card.card_id,
#             "message": card.message,
#             "likes_count": card.likes_count,
#             "board_id": board_id
#         }
#         )
#     return {
#         "board_id": board.board_id,
#         "title": board.title,
#         "owner": board.owner,
#         "cards": cards
#     }


@board_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = validate_board(board_id)

    db.session.delete(board)
    db.session.commit()

    return make_response(jsonify(f"Board {board.title} with id #{board.board_id} successfully deleted"))
