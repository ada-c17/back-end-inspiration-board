from app import db
from app.models.error_handler import Error_Handler

class Board(db.Model, Error_Handler):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    owner = db.Column(db.String, nullable=False)
    cards = db.relationship('Card', backref='board', lazy=True)
    
    def to_dict(self):
        return dict(
            board_id = self.board_id,
            title = self.title,
            owner = self.owner
        )