from flask import Blueprint, request, jsonify, make_response
from flask import abort
from app import db
from os import abort

from app.models.board import Board
from app.models.card import Card

board_bp = Blueprint("board_bp", __name__, url_prefix="/boards")

# 1. POST - Create a new board, by filling out a form. The form includes "title" and "owner" name of the board.
# POST displays ERROR msg if empty/blank/invalid/missing "title" or "owner" input.


@board_bp.route("", methods=["POST"])
def create_one_board():
    request_body = request.get_json()
    request_body = validate_board_input(request_body)

    new_board = Board(
        title=request_body['title'], owner=request_body['owner'])

    db.session.add(new_board)
    db.session.commit()
    return {
        'id': new_board.board_id,
        'title': new_board.title,
        'msg': f'{new_board.owner} created {new_board.title}'
    }, 201

# helper function:


def validate_board_input(request_body):
    if "title" not in request_body or "title" == "":
        abort(make_response(
            {"details": "Invalid data. Title missing or invalid from board"}, 400))
    if "owner" not in request_body or "owner" == "":
        abort(make_response(
            {"details": "Invalid data. Owner missing or invalid from board"}, 400))
    return request_body

# GET- Read; View a list of all boards


@board_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()
    boards_response = []
    for board in boards:
        boards_response.append({
            "id": board.board_id,
            "owner": board.owner,
            "title": board.title,
            # not returning card list at this time. May want to add in later.
        })

    return jsonify(boards_response), 200
# GET - Read; Select a specific board


@board_bp.route("/<board_id>", methods=["GET"])
def get_one_board(board_id):
    chosen_board = validate_board(board_id)

    response = {
        "id": chosen_board.board_id,
        "owner": chosen_board.owner,
        "title": chosen_board.title,
        # not returning card list at this time. May want to add in later.
    }
    return jsonify(response), 200


# GET- Read all cards in a selected board
@board_bp.route("/<board_id>/cards", methods=["GET"])
def get_all_cards_for_board(board_id):
    chosen_board = validate_board(board_id)
    chosen_board_cards = []
    for card in chosen_board.cards:
        chosen_board_cards.append({
            'card_id': card.card_id,
            'message': card.message,
            'like_count': card.like_count,
            'board_id': card.board_id
        })
    return jsonify(chosen_board_cards), 200


# Helper function to validate board_id:

def validate_board(board_id):
    try:
        board_id = int(board_id)
    except:
        abort(make_response(
            {"message": f"Board: {board_id} is not a valid board id"}, 400))
    board = Board.query.get(board_id)
    if not board:
        abort(make_response(
            {"message": f"Board: #{board_id} not found"}, 404))
    return board

# POST: Create a new card for the selected board,
# by filling out a form and filling out a "message."
# See an error message if I try to make the card's "message" more than 40 characters.
# All error messages can look like a new section on the screen, a red outline around the input field, and/or disabling the input, as long as it's visible
# See an error message if I try to make a new card with an empty/blank/invalid/missing "message."


@board_bp.route("/<board_id>/card", methods=["POST"])
def create_card_for_board(board_id):
    board = validate_board(board_id)
    request_body = request.get_json()

    if len(request_body["message"]) > 0 and len(request_body["message"]) <= 40:
        new_card = Card(
            message=request_body["message"],
            board=board,
        )
    else:
        abort(make_response(
            {"message": f"Card message for board #{board_id} too long, please keep it under 40 characters"}, 400))

    db.session.add(new_card)
    db.session.commit()

    return {
        'msg': f'Succesfully created new card for {board.title}',
        'message': new_card.message,
        'card_id': new_card.card_id,
        'like_count': new_card.like_count,
        'board_id': board_id
    }, 201


@board_bp.route('/<board_id>', methods=['DELETE'])
def delete_one_board(board_id):
    board = validate_board(board_id)

    db.session.delete(board)
    db.session.commit()

    rsp = {'msg': f'Board #{board.board_id} successfully deleted!'}
    return jsonify(rsp), 200
