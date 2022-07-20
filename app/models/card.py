from app import db
class Card(db.Model):
    __tablename__ = 'cards'
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)

    board_id = db.Column(db.Integer, db.ForeignKey("boards.board_id"))
    board = db.relationship("Board", back_populates="cards")

    def to_dict(self):
        return {
            "card_id": self.card_id,
            "message": self.message,
            "likes_count": self.likes_count
        }