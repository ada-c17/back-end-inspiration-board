from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String, nullable=False)
    likes_count = db.Column(db.Integer, nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'), nullable=False)
    board = db.relationship("Board", back_populates='cards')


    required_attributes = {
        "message" : True, 
        "board_id" : True, 
        }

    # Instance Methods
    def self_to_dict(self):
        instance_dict = dict(
            card_id=self.card_id,
            message=self.message,
            board_id=self.board_id,
            likes_count=self.likes_count
        )

        return instance_dict
    

    def update_self(self, data_dict):
        dict_key_errors = []
        for key in data_dict.keys():
            if hasattr(self, key):
                setattr(self, key, data_dict[key])
            else:
                dict_key_errors.append(key)
        if dict_key_errors:
            raise ValueError(dict_key_errors)


    # Class Methods
    

    @classmethod
    def create_from_dict(cls, data_dict):
        if data_dict.keys() == cls.required_attributes.keys():
            return cls(message=data_dict["message"],
                board_id = data_dict["board_id"],
                likes_count = 0
            )
        
        else:
            remaining_keys= set(data_dict.keys())-set(cls.required_attributes.keys())
            response=list(remaining_keys)
            raise ValueError(response)

    @classmethod
    def return_class_name(cls):
        return cls.__name__
