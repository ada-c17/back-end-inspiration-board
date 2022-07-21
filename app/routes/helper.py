from flask import abort, make_response


def validate_class_instance(instance_id, cls):
    try:
        instance_id = int(instance_id)
    except:
        return abort(make_response({"message": f'{cls.__name__} {instance_id} is invalid'}, 400))

    instance = cls.query.get(instance_id)

    if not instance:
        abort(make_response(
            {"message": f'{cls.__name__} {instance_id} not found'}, 404))

    return instance
