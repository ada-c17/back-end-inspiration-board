from flask import Blueprint, request, jsonify, make_response
from flask import abort
from app import db
from os import abort

from app.models.card import Card


cards_bp = Blueprint('cards', __name__, url_prefix='/cards')


# @cards_bp.route('', methods=['GET'])
# def get_all_cards():
#     cards = Card.query.all()
#     cards_response = []
#     for card in cards:
#         cards_response.append({
#             'message': card.message,
#             'card_id': card.card_id,
#             'like_count': card.like_count
#         })
#     return jsonify(cards_response), 200


# @cards_bp.route('/<card_id>', methods=['GET'])
# def get_one_card(card_id):
#     card = validate_card(card_id)
#     return jsonify({
#         'message': card.message,
#         'card_id': card.card_id,
#         'like_count': card.like_count
#     }), 200


@cards_bp.route('/<card_id>', methods=['PUT'])
def update_one_card(card_id):
    card = validate_card(card_id)
    try:
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
