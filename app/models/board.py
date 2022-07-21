from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    owner = db.Column(db.String, nullable=False)
    cards = db.relationship("Card", back_populates='board')


    required_attributes = {
        "title" : True,
        "owner" : True
    }

    # Instance Methods

    def self_to_dict(self):
        instance_dict = dict(
            board_id=self.board_id,
            title=self.title,
            owner=self.owner
        )
        
        card_list = [card.self_to_dict() for card in self.cards] if self.cards else []
        # sort card list by card_ids to prevent cards shifting when like numbers change
        card_list.sort(key= lambda x: x["card_id"])
        instance_dict["cards"] = card_list
        
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
            return cls(title=data_dict["title"], owner=data_dict["owner"])
        else:
            remaining_keys= set(data_dict.keys())-set("title", "owner")
            response=list(remaining_keys)
            raise ValueError(response)
    
    @classmethod
    def return_class_name(cls):
        return cls.__name__