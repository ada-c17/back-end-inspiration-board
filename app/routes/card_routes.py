from flask import Blueprint, request, jsonify, make_response
from flask import abort
from app import db
from os import abort
# import models:

from models.card import Card

# Card Model routes:
# POST: Create a new card for the selected board,
# by filling out a form and filling out a "message."
# See an error message if I try to make the card's "message" more than 40 characters.
# All error messages can look like a new section on the screen, a red outline around the input field, and/or disabling the input, as long as it's visible
# See an error message if I try to make a new card with an empty/blank/invalid/missing "message."
# GET: View a list of cards that belong to the selected board.
# DELETE: DONE.


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
