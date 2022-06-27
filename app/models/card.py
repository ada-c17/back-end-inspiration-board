from app import db

class Card (db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message= db.Column(db.String, nullable=False)
    likes_count = db.Column(db.Integer, nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'), nullable=True)
    board = db.relationship("Board", back_populates="cards")