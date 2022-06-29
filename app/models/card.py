from app import db


class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey("board.board_id"), nullable=True)
    

    def to_dict_card(self):
        response = {
            "id":self.card_id,
            "likes_count":self.likes_count,
            "message":self.message
        }
        return response


    