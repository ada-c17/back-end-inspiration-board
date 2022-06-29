from flask import Blueprint, request, jsonify, make_response, abort
from sqlalchemy import func
from app import db
from app.models.board import Board
from .card_routes import Card, validate_card

board_bp = Blueprint("board_bp", __name__, url_prefix="/boards")

#Tori changed boards.board_id to board.board_id in line 15 below.
#validation board helper function
def validate_board(board_id):
    board_id=int(board_id)
    boards = Board.query.all()
    for board in boards:
        if board_id==board.board_id:
            return board
    abort(make_response({'details': 'This Board does not exist'}, 404))

# GET /boards
@board_bp.route("", methods=["GET"])
def get_all_boards():

    params = request.args
    if not params:
        boards = Board.query.all()
    elif "title" in params:
        found_title = params["title"]
        boards = Board.query.filter(func.lower(Board.title)==func.lower(found_title))
    elif "owner" in params:
        found_owner = params["owner"]
        boards = Board.query.filter(func.lower(Board.owner)==func.lower(found_owner))
    else: 
        return {"msg": "Sorry query not found, please search elsewhere."}

    board_reply = []
    for board in boards:
        board_reply.append({"title": board.title,
                            "owner": board.owner,
                            "id": board.board_id})
    return jsonify(board_reply)

# POST /boards
@board_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    new_board = Board(title=request_body["title"],
                    owner=request_body["owner"])

    db.session.add(new_board)
    db.session.commit()

    return make_response(f"New board: '{new_board.title}' succesfully created.  YAY!", 201)


# POST /boards/<board_id>/cards
@board_bp.route('/<board_id>/cards', methods=['POST'])
def post_cards_to_specific_board(board_id):
    board = validate_board(board_id)
    # print(Card.query.all())

    request_body = request.get_json()

    new_card = Card(message=request_body['message'])
    print(new_card)

    db.session.add(new_card)
    db.session.commit()


    card_list = Card.query.all()
    print(card_list, "yes")
    cards_for_board = []

    # for card in cards:
    #     if card.new
    
    return {'card': card_list.to_dict()}, 201

    card_list = request_body["card_ids"]

    for card in card_list:
        board.cards.append(card)
    db.session.commit()

    return jsonify({
        'id': board.board_id,
        'card_ids': card_list
    }), 200


# GET /boards/<board_id>/cards
@board_bp.route('/<board_id>/cards', methods=['GET'])
def get_all_cards_for_specific_board(board_id):
    board = validate_board(board_id)

    card_list = []

    for card in board.cards:
        card_list.append(card.to_dict())

    return jsonify({
        'id': board.board_id,
        'message': board.message
    }), 200