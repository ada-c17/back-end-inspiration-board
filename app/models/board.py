from app import db
class Board(db.Model):
    __tablename__ = 'boards'
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)

    cards = db.relationship("Card", back_populates="boards")