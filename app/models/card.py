from app import db


class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    boards = db.relationship("Board", backref ="card", lazy = True)
    # I checked how to use laze in this website...
    #https://medium.com/@ns2586/sqlalchemys-relationship-and-lazy-parameter-4a553257d9ef