from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from app.helper_functions import *

card_bp = Blueprint('Cards', __name__, url_prefix='/cards')


@card_bp.route("/<card_id>", methods=["PATCH"])
def update_card(card_id):
    card = get_record_by_id(Card, card_id)

    request_body = request.get_json()

    update_record_safely(Card, card, request_body)

    db.session.commit()

    return return_database_info_dict("card", card.self_to_dict())

#deleting one card
@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_one_card(card_id):
    card = get_record_by_id(Card, card_id)
    db.session.delete(card)
    db.session.commit()
    
    return success_message_info_as_list(dict(details=f'Card {card.card_id} \"{card.message}\" successfully deleted'))

