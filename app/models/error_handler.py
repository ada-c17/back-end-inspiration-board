from flask import jsonify, abort, make_response, request



class Error_Handler(): 
    @classmethod 
    def validate(cls, id):
        from ..routes import error_message

        try: 
            id = int(id)
        except:
            error_message(f'{cls.__name__.lower()} {id} is an invalid id', 400)     

        valid = cls.query.get(id) 
        
        if not valid: 
            error_message(f'{cls.__name__.lower()} {id} is missing', 404)
        return valid 