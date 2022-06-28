from flask import Blueprint, request, jsonify, make_response
from flask import abort  # added for validations
from app import db
from os import abort
# import models:
from .models.board import Board
from .models.card import Card

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint("board_bp", __name__, url_prefix="/boards")

# Board Model routes:

# 1. POST - Create a new board, by filling out a form. The form includes "title" and "owner" name of the board.
# POST displays ERROR msg if empty/blank/invalid/missing "title" or "owner" input.


@board_bp.route("", methods=["POST"])
def create_one_board():
    request_body = request.get_json()
    try:
        # need to add validating here
        new_board = Board(
            title=request_body['title'], owner=request_body['owner'])
    except:
        abort(make_response(
            {"details": "Invalid data. Title or owner missing or invalid from board"}, 400))
    db.session.add(new_board)
    db.session.commit()
    return {
        'id': new_board.id,
        'msg': f'New board {new_board.title} created'
    }, 201

# 2.GET- Read; View a list of all boards
# 3. GET - Read; Select a specific board

# Helper function to validate board_id:


def validate_board(board_id):
    try:
        board_id = int(board_id)
    except:
        abort(make_response(
            {"message": f"Planet: {board_id} is not a valid board id"}, 400))
    board = Board.query.get(board_id)
    if not board:
        abort(make_response(
            {"message": f"Board: #{board_id} not found"}, 404))
    return board


# Card Model routes:
cards_bp = Blueprint('cards', __name__, url_prefix='/cards')


@cards_bp.route('', methods=['POST'])
def create_one_card():
    if not request.is_json:
        return {'msg': 'Missing json request body'}, 400
    request_body = request.get_json()
    try:
        message = request_body['message']
        like_count = request_body['like_count']
    except KeyError:
        return {'msg': 'failed to create new planet due to missing attributes'}, 400

    new_card = Card(message=message,
                    like_count=like_count)
    db.session.add(new_card)
    db.session.commit()

    rsp = {'msg': f'Succesfully created planet with id {new_card.card_id}'}
    return jsonify(rsp), 201


@cards_bp.route('', methods=['GET'])
def get_all_cards():
    cards = Card.query.all()
    cards_response = []
    for card in cards:
        cards_response.append(card.get_dict())

    return jsonify(cards_response), 200


@cards_bp.route('/<card_id>', methods=['GET'])
def get_one_card(card_id):
    card = validate_card(card_id)

    return jsonify(card.get_dict()), 200


@cards_bp.route('/<card_id>', methods=['PUT'])
def update_one_card(card_id):
    card = validate_card(card_id)

    if not request.is_json:
        return {'msg': 'Missing json request body'}, 400

    request_body = request.get_json()
    try:
        card.message = request_body['message']
        card.like_count = request_body['like_count']
    except KeyError:
        return {
            'msg': 'Update failed. message and like_count are required!'
        }, 400

    db.session.commit()

    rsp = {"msg": f"Card #{card_id} successfully updated!"}
    return jsonify(rsp), 200


@cards_bp.route('/<card_id>', methods=['DELETE'])
def delete_one_card(card_id):
    card = validate_card(card_id)

    db.session.delete(card)
    db.session.commit()

    rsp = {'msg': f'Card #{card.card_id} successfully deleted!'}
    return jsonify(rsp), 200


def validate_card(card_id):
    try:
        card_id = int(card_id)
    except:
        rsp = {"msg": f"Card with id {card_id} is invalid."}
        abort(make_response(rsp, 400))

    card = Card.query.get(card_id)

    if not card:
        rsp = {'msg': f'Could not find card with id {card_id}.'}
        abort(make_response(rsp, 404))

    return card
