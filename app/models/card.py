from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(100), nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'), nullable=False)
    board = db.relationship('Board', back_populates='cards', lazy=True)

    def to_dict(self):
        return {
            'id': self.card_id,
            'message': self.message,
            'likes': self.likes,
            'board_id': self.board_id
        }
    