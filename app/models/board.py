from flask import abort, make_response
from app import db

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    theme = db.Column(db.String)
    cards = db.relationship("Card", back_populates="board", lazy = True)

    def as_dict(self):
        return {
            'board_id': self.id,
            'title': self.title,
            'owner': self.owner,
            'theme': self.theme,
            'cards': [card.as_dict() for card in self.cards]
        }
    
    @classmethod
    def validate_and_get_by_id(cls, id):
        try:
            id = int(id)
        except:
            abort(make_response({
                "message": f"{id} is not a valid id"
                }, 400))
        
        board = cls.query.get(id)
        if board is None:
            abort(make_response({
                "message":f"Board with id of {id} was not found"
                }, 404))
        
        return board
