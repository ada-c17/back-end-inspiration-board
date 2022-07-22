from flask import abort, make_response
from app import db

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    board = db.relationship("Board", back_populates="cards")
    
    def as_dict(self):
        return {
            'card_id': self.id,
            'message': self.message,
            'likes_count': self.likes_count,
            'board_id': self.board_id
        }

    @classmethod
    def validate_and_get_by_id(cls, id):
        try:
            id = int(id)
        except:
            abort(make_response({
                "message": f"{id} is not a valid id"
                }, 400))
        
        card = cls.query.get(id)
        if card is None:
            abort(make_response({
                "message":f"Card with id of {id} was not found"
                }, 404))
        
        return card