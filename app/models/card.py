from app import db

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.VARCHAR(40), nullable=False)
    likes_count = db.Column(db.Integer, default=0)
    board_id = db.Column(db.Integer, db.ForeignKey("board.id"), nullable=False)
    board = db.relationship("Board", back_populates="cards")

    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "likes_count": self.likes_count,
            "board_id": self.board_id,
            } 