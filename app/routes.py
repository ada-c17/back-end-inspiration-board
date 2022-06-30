from app.models.board import Board
from app.models.card import Card
from flask import Blueprint, request, jsonify, make_response
from app import db
import requests

# example_bp = Blueprint('example_bp', __name__)

boards_bp = Blueprint("boards", __name__,url_prefix="/boards")
cards_bp = Blueprint("cards", __name__,url_prefix="/cards")



    # ************************************Routes for Boards*************************************
def validate_board(board_id):
    try:
       board_id = int(board_id)
    except:
        abort(make_response({"message":f"board {board_id} invalid"}, 400))

    board = Board.query.get(board_id)

    if not board:
        abort(make_response({"message":f"board {board_id} not found"}, 404))

    return board



#Create one board
@boards_bp.route("", methods=["POST"])
def create_new_board():
   
        request_body = request.get_json()
        if "title" not in request_body or "owner" not in request_body:
             return make_response({"details":f"Invalid data"}, 400)

        new_board = Board(title=request_body["title"],
                        owner=request_body["owner"],
                        )

        db.session.add(new_board)
        db.session.commit()
        return jsonify({"board":new_board.to_json()}),201





# Read all boards
@boards_bp.route("", methods=["GET"])
def get_boards():
 
    boards= Board.query.all()
    board_response = []
    
    for board in boards:
        board_response.append(board.to_json())
    
    return make_response( jsonify(board_response),200)


#Delete one board
@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = validate_board(board_id)

    db.session.delete(board)
    db.session.commit()

    return make_response({"details":f'Board {board.board_id} \"{board.title}\" successfully deleted'}),200


    # ************************************Routes for Cards**************************************

    def validate_card(card_id):
        try:
            card_id = int(card_id)
        except:
            abort(make_response({"message":f"card {card_id} invalid"}, 400))

        card = Card.query.get(card_id)

        if not card:
            abort(make_response({"message":f"card {card_id} not found"}, 404))

        return card
    
    
    
    
    #Create one card
@cards_bp.route("", methods=["post"])
def create_new_card():
   
        request_body = request.get_json()
        if "title" not in request_body or "owner" not in request_body:
            return {
        "details": "Invalid data"
    },400
        new_card = Card(title=request_body["title"], owner=request_body["owner"]
                        )


        db.session.add(new_card)
        db.session.commit()

        return {"card":{"id":new_card.card_id, "title":new_card.title}},201




#Update one card//?????????????????with id
@cards_bp.route("/<card_id>", methods=["PUT"])
def update_card(card_id):
    card = validate_card(card_id)

    request_body = request.get_json()

    card.title = request_body["title"]
    card.owner = request_body["owner"]
    

    db.session.commit()

    return make_response(jsonify(f"card #{card.card_id} successfully updated")),200


#Delete one card
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_card(card_id)

    db.session.delete(card)
    db.session.commit()

    return {"details":f"card {card.card_id} \"{card.title}\" successfully deleted"}

