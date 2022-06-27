from app import db

class Card(db.Model):
	card_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	message = db.Column("message",db.String, nullable = False)
	likes_count = db.Column("likes_count", db.Integer, default = 0)
	board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))
	board = db.relationship("Board", back_populates = "cards")