from app import db
from flask import jsonify

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    creator = db.Column(db.String)
    cards = db.relationship("Card", back_populates="board")

    def to_json(self):
        return dict(
            boardId = self.board_id,
            title = self.title,
            creator = self.creator,
            cards = [card.to_json() for card in self.cards]
        )

    @classmethod
    def from_json(cls, json_data):
        return cls(
            title = json_data["title"],
            creator = json_data["creator"]
        )
# if we want to update records
    # def replace_details(self, data_dict):
    #     self.title = data_dict["title"]
    #     self.creator = data_dict["creator"]