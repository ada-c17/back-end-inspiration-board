from app import db
from flask import abort, make_response

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    cards = db.relationship("Card", backref="board", lazy=True)

    def make_json(self):
        board_dic = {
            "id": self.board_id,
            "title": self.title,
            "owner": self.owner,
        }    
        return board_dic

    def make_json_with_cards(self):
        board_dic = {
            "id": self.board_id,
            "title": self.title,
            "owner": self.owner,
            "cards": [card.to_dict() for card in self.cards],
        }
        return board_dic

    @classmethod
    def valid_board(cls, request_body):
        try:
            try:
                new_board = cls(title = request_body["title"], description = request_body["owner"])
            except KeyError:
                new_board = cls(
                title=request_body['title'],
                owner=request_body['owner'])
            return new_board
        except KeyError:
            abort(make_response({"details": "Invalid data"}, 400)) 







