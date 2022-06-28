from app import db


class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    like_count= db.Column(db.Integer)

    def get_dict(self):
        return  {
                'card_id' : self.card_id,
                'message' :  self.message,
                'like_count' : self.like_count
            }
