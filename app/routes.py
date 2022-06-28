from flask import Blueprint, request, jsonify, make_response
from app import db

# example_bp = Blueprint('example_bp', __name__)


def validate_record(cls, id):
    try:
        id = int(id)
    except ValueError:
        abort(make_response({"message": f"{cls} {id} is invalid"}, 400))

    obj = cls.query.get(id)

    if not obj:
        return abort(make_response({"message": f"{cls.__name__} {id} not found"}, 404))

    return obj



