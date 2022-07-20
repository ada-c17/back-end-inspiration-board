from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    message = db.Column(db.String(40), nullable= False)
    likes_count = db.Column(db.Integer, default = 0)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'), nullable=False)
    board = db.relationship("Board", back_populates ="cards", lazy=True)

    def to_dict(self):
        return {
            "id": self.card_id,
            "message": self.message,
            "likes_count": self.likes_count,
        }

    @classmethod
    def create_card(cls, request_body):
        new_card = cls(message = request_body["message"])

        return new_card
