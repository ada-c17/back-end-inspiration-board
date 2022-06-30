from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship("Card", back_populates="board")

    #? do we want to include a method or two here to convert a Board to a dictionary or something? How will the frontend use board data?
    def to_dict(self):
        return {
            "id": self.board_id,
            "title": self.title,
            "owner": self.owner,
            } 