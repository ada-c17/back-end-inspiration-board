from app import db
from flask import make_response, abort


class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    like_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))
    board = db.relationship("Board", back_populates="cards")

    def to_json(self):
        return {
            "id": self.card_id,
            "message": self.message,
            "like_count": self.like_count,
            "board_id": self.board_id,
            "board": self.board.title
        }

    @classmethod
    def create(cls, board_id, request_body):
        if "message" not in request_body:
            return abort(make_response({"message": "Must include message for card in request"}, 400))
        return cls(message=request_body["message"], board_id=board_id, like_count=0)

    # UPDATE Card
    def update(self, request_body):
        self.message = request_body["message"]
