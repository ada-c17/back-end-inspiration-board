from flask import jsonify, abort, make_response 

def error_msg(message, status_code):
    abort(make_response(jsonify(dict(details=message)), status_code))

def success_msg(message, status_code):
    return make_response(jsonify(dict(details=message)), status_code)

def make_model(cls, data_dict, **kwargs):
    try: 
        model = cls.from_dict(data_dict, **kwargs)
    except KeyError as err:
        print(err)
        error_msg("Invalid data", 400)

    return model

def get_model_by_id(cls, id):
    try:
        id = int(id)
    except ValueError:
        error_msg(f"Invalid id {id}", 400)

    model = cls.query.get(id)
    if model:
        return model
    
    error_msg(f"No {cls.__name__} data with id: {id}", 404)