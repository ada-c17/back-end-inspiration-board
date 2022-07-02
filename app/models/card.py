from email.policy import default
from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, nullable=False)
    message = db.Column(db.String, nullable=False)
    likes_count = db.Column(db.Integer, default=0)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'), nullable=False)
    board = db.relationship("Board", back_populates="cards")

    def to_dict(self):
        return dict(
            id = self.card_id,
            message = self.message,
            likes_count = self.likes_count,
            board_id = self.board_id
        )
