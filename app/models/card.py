from app import db

#this is new
class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer, default=0)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'), nullable=False)
    board = db.relationship('Board', back_populates='cards')

    def to_dict(self):
            
            card_dict = {
                'id': self.card_id,
                'message': self.message,
                'likes_count': self.likes_count,
            }
            
            return card_dict