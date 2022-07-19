from flask import Blueprint, request, jsonify, make_response
from flask import abort
from app import db
from os import abort

from app.models.card import Card


cards_bp = Blueprint('cards', __name__, url_prefix='/cards')

# Is this really necessary?  Cards also made through: board_bp.route("/<board_id>/card", methods=["POST"])


@cards_bp.route('', methods=['POST'])
def create_one_card():
    if not request.is_json:
        return {'msg': 'Missing json request body'}, 400
    request_body = request.get_json()
    try:
        message = request_body['message']
    except KeyError:
        return {'msg': 'failed to create new card due to missing attributes'}, 400

    new_card = Card(message=message)
    # like_count=like_count)
    db.session.add(new_card)
    db.session.commit()
    response = {
        'msg': 'Succesfully created new card',
        'message': new_card.message,
        'card_id': new_card.card_id,
        'like_count': new_card.like_count
    }
    return jsonify(response), 201


@cards_bp.route('', methods=['GET'])
def get_all_cards():
    cards = Card.query.all()
    cards_response = []
    for card in cards:
        cards_response.append({
            'message': card.message,
            'card_id': card.card_id,
            'like_count': card.like_count
        })
    return jsonify(cards_response), 200


@cards_bp.route('/<card_id>', methods=['GET'])
def get_one_card(card_id):
    card = validate_card(card_id)
    return jsonify({
        'message': card.message,
        'card_id': card.card_id,
        'like_count': card.like_count
    }), 200


@cards_bp.route('/<card_id>', methods=['PUT'])
def update_one_card(card_id):
    card = validate_card(card_id)
    # if not request.is_json:
    #     return {'msg': 'Missing json request body'}, 400
    # request_body = request.get_json()
    try:
        # card.message = request_body['message']
        card.like_count += 1
    except KeyError:
        return {
            'msg': 'Update failed. like_count is required!'
        }, 400

    db.session.commit()
    return jsonify({
        'message': card.message,
        'card_id': card.card_id,
        'like_count': card.like_count
    }), 200


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
