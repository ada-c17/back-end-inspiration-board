from app import db
from .card import Card

class Board(db.Model):
	board_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	title = db.Column(db.String, nullable = False)
	owner = db.Column(db.String, nullable = False)
	cards = db.relationship("Card", back_populates = "board", lazy = True)
	color = db.Column(db.String, nullable = False)
	
	def to_json(self):
		cards = [item.to_json() for item in self.cards]
		return {"board_id": self.board_id,
                "title": self.title,
				'owner': self.owner,
				'cards': cards,
				"color": self.color
            }
			
	@classmethod
	def create(cls, req_body):
		new_board = cls(
			title = req_body['title'],
			owner=req_body['owner'],
			color=req_body["color"]
			#cards=[]
		)
		return new_board	
