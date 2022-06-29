from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from .models.board import Board
from .models.card import Card

# example_bp = Blueprint('example_bp', __name__)
boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")
# cards_bp = Blueprint("cards_bp", __name__, url_prefix="/cards")



def error_message(message, status_code):
    abort(make_response({"details":message}, status_code))

@boards_bp.route("", methods=["GET"])
def get_boards():
    boards = Board.query.all()
    boards_response = [board.to_dict() for board in boards]

    return jsonify(boards_response)

@boards_bp.route('', methods=['POST'])
def create_board():
    request_body = request.get_json()

    if not "title" in request_body or not "owner" in request_body:  # or \
        # not "completed_at" in request_body:
        return jsonify({
            "details": "Invalid data"
        }), 400

    new_board = Board(title=request_body["title"],
                    owner=request_body["owner"]
                    )

    db.session.add(new_board)
    db.session.commit()

    return {
        "board": new_board.to_dict()
    }, 201

@boards_bp.route("/<board_id>", methods=["GET"])
def get_board_by_id(board_id):
    # board = Board.query.get(board_id)
    board = Board.validate(board_id)


    # if board:
    return {"board": board.to_dict()}
    
    # else:
    #     return jsonify({
    #         "details": f"ID {board_id} does not exist"
    #     }), 404

@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_all_cards_on_board(board_id):

    board = Board.validate(board_id)

   
    cards = board.cards
    list_of_cards = []
    for card in cards:
        list_of_cards.append(card.to_dict())

    return {"cards": list_of_cards}

    # response_body = {"board_id": board.board_id, "title": board.title, "cards": list_of_cards}
    # return make_response(jsonify(response_body), 200)

@boards_bp.route("/<id>/cards", methods=["POST"])
def add_card_to_board(id):
    board = Board.validate(id)
    
    request_body = request.get_json()
    
    if len(request_body["message"]) > 40: 
        error_message("Message must be less than 40 characters", 400)



        

    new_card = Card(board_id=id,
                message=request_body["message"]
                )
    db.session.add(new_card)
    db.session.commit()

    response_body = {"id": new_card.card_id, "board_id": new_card.board_id, "message": new_card.message}
    return make_response(jsonify(response_body), 200)

@boards_bp.route("/<board_id>/cards/<card_id>", methods=["DELETE"])
def delete_card_by_id(board_id, card_id):
    # card = Card.query.get(card_id)
    card = Card.validate(card_id)

    
    db.session.delete(card)
    db.session.commit()

    return make_response(dict(details=f'Card {card.card_id} "{card.message}" successfully deleted'), 200)
