from app import db

class Boad(db.Model):
    board_id = db.Column(db.Integer, primar_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
