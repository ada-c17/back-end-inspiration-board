from app import db
from flask import make_response, abort

class Card (db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message= db.Column(db.String, nullable=False)
    likes_count = db.Column(db.Integer, nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'), nullable=True)
    board = db.relationship("Board", back_populates="cards")

        
    def to_json(self):
            return {"cardId" : self.card_id,
                    "message" : self.message,
                    "likesCount": self.likes_count,
                    "boardId": self.board_id}

    def update_card(self, update_body):

        # self.card_id = update_body["cardId"]
        # self.message = update_body["message"]
        self.likes_count = update_body["likesCount"]
        # self.board_id = update_body["boardId"]

    @classmethod
    def from_json(cls, request_body):

        if len(request_body["message"]) > 40:
            abort(make_response({"details": "Message is too long"}, 400))

        new_card = cls(
            message=request_body["message"],
            likes_count = request_body["likesCount"],
            board_id = request_body["boardId"], 
            )

        return new_card