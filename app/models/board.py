from app import db
from flask import make_response, abort
# from .card import Task
# from app.routes.helpers import validate_model_instance 

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title= db.Column(db.String, nullable=False)
    owner = db.Column(db.String, nullable=False)
    cards = db.relationship("Card", back_populates = "board", lazy = True)
    
    def to_json(self):
            return {"boardId" : self.board_id,
                    "title" : self.title,
                    "owner": self.owner,}

    @classmethod
    def from_json(cls, request_body):

        if ("title" or "owner") not in request_body:
            abort(make_response({"details": "Invalid data"}, 400))

        new_goal = cls(
            title=request_body["title"],
            owner=request_body["owner"])

        return new_goal
