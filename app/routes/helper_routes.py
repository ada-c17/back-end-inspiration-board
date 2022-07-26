from flask import make_response, abort, jsonify

def validate_id(cls, id):
        try:
            id = int(id)
        except ValueError:
            abort(make_response(jsonify(f"{cls.__name__} {id} is invalid"), 400))
        instance = cls.query.get(id)
        if not instance:
            abort(make_response(jsonify(f"{cls.__name__} {id} not found"), 404))
        return instance

def validate_request(request, *attributes):
    request_body = request.get_json()
    for attribute in attributes:
        try:
            request_body[attribute]
        except KeyError:
            abort(make_response({"details": "Invalid data"}, 400)) 
    return request_body

def error_message(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))