from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    owner = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.board_id,
            "title": self.title,
            "owner": self.owner
        }

    @classmethod
    def create(cls, req_body):
        new_board = cls (
            title = req_body["title"],
            owner = req_body["owner"]
        )

        return new_board