from app import db

class Card(db.Model):
	card_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	message = db.Column("message",db.String, nullable = False)
	likes_count = db.Column("likes_count", db.Integer, default = 0)
	board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))
	board = db.relationship("Board", back_populates = "cards")

	def update(self, request_body):
		self.message = request_body["message"]
		self.likes_count = request_body["likes_count"]
            