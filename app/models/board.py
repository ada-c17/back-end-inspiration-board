from app import db
from flask import make_response, abort, request
from .card import Card

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title= db.Column(db.String, nullable=False)
    owner = db.Column(db.String, nullable=False)
    cards = db.relationship("Card", back_populates = "board", lazy = True)
    
    def to_json(self):
            return {"boardId" : self.board_id,
                    "title" : self.title,
                    "owner": self.owner,}

    def link_card_to_board(self, request_body):

        new_card = Card.from_json(request_body)
        if new_card not in self.cards:
            self.cards.append(new_card)
        
        return new_card

    @classmethod
    def from_json(cls, request_body):

        if "title" not in request_body or "owner" not in request_body:
            abort(make_response({"details": "Invalid data"}, 400))

        new_board = cls(
            title=request_body["title"],
            owner=request_body["owner"])

        return new_board
