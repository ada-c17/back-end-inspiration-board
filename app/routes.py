from app.models.card import Card
from app.models.board import Board
from flask import Blueprint, request, jsonify, make_response, jsonify, abort
from app import db


#----------------BOARD---------------------
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

@boards_bp.route("", methods=["POST"])
def post_board():
    
    post_dict = request.get_json()
    
    if 'title' not in post_dict or 'owner' not in post_dict:
        return make_response({"details":"Invalid data"},400)
    
    title = post_dict['title']
    owner = post_dict['owner']
    board = Board(title=title, owner=owner) 
    db.session.add(board)
    db.session.commit()

    board_dict={}
    board_dict['id'] = board.id
    board_dict['title'] = board.title
    board_dict['owner'] = board.owner
    return_dict = {"board": board_dict}
    return jsonify(return_dict), 201

#------------GET ALL BOARDS---------------
@boards_bp.route("", methods=["GET"]) 
def get_all_boards():
    
    board_db = Board.query.all()  

    board_dict = {}
    boards_response = [] 
    for board in board_db:  
        board_dict = {'id': board.id,
                'title': board.title,
                'owner':board.owner
    }             
        boards_response.append(board_dict)
    return jsonify(boards_response), 200  

#-----------------------------------
@boards_bp.route("/<id>",methods = ["GET"]) 
def get_board_by_id(id):
    # Remember that id from the request is a string and not an integer

    board = Board.query.get(id)
    if (board == None):
        abort(make_response({"message":f"goal {id} not found"}, 404))
    else:
        board_dict={}
        board_dict['id'] = board.id
        board_dict['title'] = board.title
        board_dict['owner'] = board.owner
        return_dict = {"board": board_dict}
        return jsonify(return_dict), 200

#------------PUT Method - update board by id---------
@boards_bp.route("/<id>", methods=["PUT"])
def update_board_by_id(id):
    board = Board.query.get(id)
    
    if (board == None):
        abort(make_response({"message":f"board {id} not found"}, 404))

    update_dict = request.get_json()
    if 'title' not in update_dict or 'owner' not in update_dict:
        return make_response({"details":"Invalid data"},400)

    title = update_dict['title']
    owner = update_dict['owner']
    board.title = title
    board.owner = owner
    
    db.session.commit()

    board_dict={}
    board_dict['id'] = board.id
    board_dict['title'] = board.title
    board_dict['owner'] = board.owner
    
    return_dict = {"goal": board_dict}
    return jsonify(return_dict), 200

#------------remove board by id------------
@boards_bp.route("/<id>", methods=["DELETE"])
def remove_board_by_id(id):
    board = Board.query.get(id)
    
    if (board == None):
        abort(make_response({"message":f"board {id} not found"}, 404))
    
    db.session.delete(board)
    db.session.commit()
    return make_response({"details":f"Board {id} \"{board.title}\" successfully deleted"},200)

#------------------------------------------------

cards_bp = Blueprint("cards", __name__, url_prefix="/boards")
#-----post_card------

@cards_bp.route("/<id>/cards", methods=["POST"])
def post_card(id):
    post_dict = request.get_json()
    
    if 'message' not in post_dict:
        return make_response({"details":"invalid data"},400)
    
    message = post_dict['message']
    likes_count = 0
    board_id = int(id)

    # board = Board.query.get(board_id)

    card = Card(message = message, likes_count = likes_count, board_id = board_id)
    db.session.add(card)
    db.session.commit()

    card_dict = {}
    card_dict['card_id'] = card.card_id
    card_dict['message'] = card.message
    card_dict['likes_count'] = card.likes_count
    card_dict['board_id'] = card.board_id
    return_dict = {"card": card_dict}
    return jsonify(return_dict),201

#------get card by id --------
@cards_bp.route("/<id>",methods = ["GET"]) 
def get_card_by_id(id):
    # Remember that id from the request is a string and not an integer
    card = Card.query.get(id)
    if (card == None):
        abort(make_response({"message":f"card {id} not found"}, 404))
    
    card_dict={}
    card_dict['id'] = card.id
    card_dict['message'] = card.message
    card_dict['likes_count'] = card.likes_count
    card_dict['board_id'] = card.board_id
    return_dict = {"card": card_dict}
    return jsonify(return_dict), 200
#------------remove card by id------------
@cards_bp.route("/<id>", methods=["DELETE"])
def remove_card_by_id(id):
    card = Card.query.get(id)

    if (card == None):
        abort(make_response({"message":f"card {id} not found"}, 404))
    
    db.session.delete(card)
    db.session.commit()
    return make_response({"details":f"Card {id} \"{card.message}\" successfully deleted"},200)
    
#------------PUT Method - update card by id---------
@cards_bp.route("/<id>", methods=["PUT"])
def update_card_by_id(id):
    card = Card.query.get(id)

    if (card == None):
        abort(make_response({"message":f"card {id} not found"}, 404))
    update_dict = request.get_json()
    
    if 'message' not in update_dict or 'likes_count' not in update_dict:
        return make_response({"details":"Invalid data"},400)
    
    message = update_dict['message']
    likes_count = update_dict['likes_count']

    card.message = message
    card.likes_count = likes_count
    
    db.session.commit()

    card_dict={}
    card_dict['id'] = card.id
    card_dict['message'] = card.message
    card_dict['likes_count'] = card.likes_count
    
    return_dict = {"card": card_dict}
    return jsonify(return_dict), 200

