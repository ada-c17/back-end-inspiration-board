from app import db


class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owner = db.Column(db.String)
    
    def to_dict(self):
        board_dict = {
        "id": self.board_id,
        "title": self.title,
        "owner": self.owner,
        }
        
        # if self.goal_id:
        #     task_dict["goal_id"] = self.goal_id
        return board_dict
