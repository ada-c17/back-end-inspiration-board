from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship("Card", back_populates="board" )

    @classmethod
    def create(cls, req_body):
        new_board = cls(
            title=req_body["title"],
            owner=req_body["owner"],
        )
        return new_board

    def to_json(self):
        return {
            "board_id": self.board_id,
            "title": self.title,
            "owner": self.owner
        }