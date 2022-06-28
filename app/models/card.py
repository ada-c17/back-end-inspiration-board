from app import db

class Card(db.Model):    
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String, nullable = False)
    likes_count = db.Column(db.Integer, nullable = True)