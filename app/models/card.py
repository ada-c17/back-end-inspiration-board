from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(40), nullable=False)
    likes_count = db.Column(db.Integer, autoincrement=True)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))
    board = db.relationship('Board',back_populates='cards')

    def to_dict(self):
        return {
            "card_id": self.card_id,
            "message": self.message,
            "likes_count": self.likes_count
        }

    @classmethod
    def create(cls, request_body):
        return cls(
            message=request_body["message"],
            likes_count=request_body["likes_count"]
            )
