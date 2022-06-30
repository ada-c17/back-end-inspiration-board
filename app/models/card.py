from app import db
from app.models.error_handler import Error_Handler



class Card(db.Model, Error_Handler):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(40), nullable=False)
    likes_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))

    def to_dict(self):
        return dict(
            board_id = self.board_id,
            card_id = self.card_id,
            message = self.message,
        )

