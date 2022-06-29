from app import db


class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey("board.board_id"), nullable=True)
    # I checked how to use laze in this website...
    #https://medium.com/@ns2586/sqlalchemys-relationship-and-lazy-parameter-4a553257d9ef

    def to_dict(self):
        return {
            "id": self.card_id, 
            "message": self.message, 
            "likes_count": self.likes_count,
        }