from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card


def validate_or_abort_card(card_id):
    # returns 400 error if invalid board_id (alpha/non-int) 
    try:
        card_id = int(card_id)
    except ValueError:
        abort(make_response({"error": f"{card_id} is an invalid card id"}, 400))
    
    # returns 404 error if board_id not found in database
    card = Card.query.get(card_id)
    if not card:
        abort(make_response({"error": f"Board {card_id} not found"}, 404))
    return card