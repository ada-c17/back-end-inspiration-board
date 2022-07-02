from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    owner = db.Column(db.String, nullable=False)

    def to_dict(self):
        return dict(
            id = self.board_id,
            title = self.title,
            owner = self.owner
        )
