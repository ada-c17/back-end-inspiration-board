from email import message
from app import db
from flask import jsonify

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String, nullable=False)
    likes_count = db.Column(db.Integer, default=0)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))
    board = db.relationship("Board", back_populates="cards")

    def to_json(self):
        return dict(
            cardId = self.card_id,
            message = self.message,
            likes_count = self.likes_count
        )
