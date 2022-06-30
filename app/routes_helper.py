from flask import jsonify, abort, make_response
from app.models.board import Board
from app.models.card import Card

def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

def get_record_by_id(cls, id):
    try:
        id = int(id)
    except ValueError:
        error_message(f"Invalid id {id}", 400)

    model = cls.query.get(id)
    if model:
        return model

    error_message(f"No model of type {cls} with id {id} found", 404)

def make_record_safely(cls, data_dict):
    try:
        return cls.from_json(data_dict)
    except KeyError as err:
        error_message(f"Missing key: {err}", 400)

# if we want to update records
# def update_record_safely(cls, data_dict):
#     try:
#         cls.replace_details(data_dict)
#     except KeyError as err:
#         error_message(f"Missing key: {err}", 400)
