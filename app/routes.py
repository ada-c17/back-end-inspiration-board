from flask import make_response, abort
from app import db

def validate_record(cls, id):
    try:
        id = int(id)
    except ValueError:
        abort(make_response({"message": f"{cls} {id} is invalid"}, 400))

    obj = cls.query.get(id)

    if not obj:
        return abort(make_response({"message": f"{cls.__name__} {id} not found"}, 404))

    return obj



