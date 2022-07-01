from app import db

class Card(db.Model):    
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String, nullable = False)
    likes_count = db.Column(db.Integer, nullable = True, default=0)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'), nullable=True)
    
    def to_json(self):
        return {
            "id": self.card_id,
            "message": self.message,
            "likes": self.likes_count,}