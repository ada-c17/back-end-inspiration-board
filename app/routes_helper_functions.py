from flask import jsonify, abort, make_response
from .models.board import Board
from .models.card import Card

def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

def validate_model(model, id):
    if model == Board:
        model_name = "Board"
    elif model == Card:
        model_name = "Card"

    try:
        id = int(id)
    except:
        error_message(f"{model_name} #{id} is invalid", 400)

    model_instance = model.query.get(id)

    if not model_instance:
        error_message(f"{model_name} #{id} is not found", 404)

    return model_instance
