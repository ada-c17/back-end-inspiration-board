from app.models.card import Card
from app.models.board import Board
from flask import Blueprint, request, jsonify, make_response, jsonify, abort
from app import db


#----------------BOARD---------------------
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

@boards_bp.route("", methods=["POST"])
def post_board():
    
    post_dict = request.get_json()
    title = post_dict.get('title', None)
    owner = post_dict.get('owner', None)
    
    if not title or not owner:
        abort(make_response({
            "message":"Invalid data: New board must have a title and an owner"
            }, 400))
    
    board = Board(title=title, owner=owner)
    db.session.add(board)
    db.session.commit()

    board_dict={}
    board_dict['id'] = board.id
    board_dict['title'] = board.title
    board_dict['owner'] = board.owner
    return_dict = {
        "message": f"Board with id of {board.id} successfully created",
        "board": board_dict
        }
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
    return jsonify({"boards": boards_response}), 200  

#-----------------------------------
@boards_bp.route("/<id>", methods=["GET"]) 
def get_board_by_id(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"{id} is not a valid id"}, 400))

    board = Board.query.get(id)
    if (board == None):
        abort(make_response({"message":f"Board with id {id} not found"}, 404))

    board_dict={}
    board_dict['id'] = board.id
    board_dict['title'] = board.title
    board_dict['owner'] = board.owner
    return_dict = {"board": board_dict}
    return jsonify(return_dict), 200

#------------Update board details---------
@boards_bp.route("/<id>", methods=["PATCH"])
def update_board_by_id(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"{id} is not a valid id"}, 400))
    
    board = Board.query.get(id)
    if (board == None):
        abort(make_response({"message": f"board {id} not found"}, 404))

    update_dict = request.get_json()

    for k, v in update_dict.items():
        if k in {'title', 'owner'}:
            setattr(board, k, v)
    
    db.session.commit()

    board_dict={}
    board_dict['id'] = board.id
    board_dict['title'] = board.title
    board_dict['owner'] = board.owner
    
    return_dict = {
        "message": f"Board with id of {board.id} successfully updated",
        "board": board_dict
        }
    return jsonify(return_dict), 200

#------------remove board by id------------
@boards_bp.route("/<id>", methods=["DELETE"])
def remove_board_by_id(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"{id} is not a valid id"}, 400))
    board = Board.query.get(id)
    
    if (board == None):
        abort(make_response({"message":f"board {id} not found"}, 404))
    
    db.session.delete(board)
    db.session.commit()
    return jsonify({
        "message":f"Board {id} \"{board.title}\" successfully deleted"
        }, 200)

#-----------------CARD--------------------------

cards_bp = Blueprint("cards", __name__, url_prefix="/boards")

#-----post_card------
@cards_bp.route("/<id>/cards", methods=["POST"])
def post_card(id):
    post_dict = request.get_json()
    message = post_dict.get('message', None)
    
    if not message:
        abort(make_response({
            "message": "Invalid data: New card needs a message"
            }, 400))
    
    likes_count = 0
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"{id} is not a valid id"}, 400))
    board = Board.query.get(id)
    
    if (board == None):
        abort(make_response({"message":f"board {id} not found"}, 404))

    card = Card(message = message, likes_count = likes_count, board_id = board.id)
    db.session.add(card)
    db.session.commit()

    card_dict = {}
    card_dict['id'] = card.id
    card_dict['message'] = card.message
    card_dict['likes_count'] = card.likes_count
    card_dict['board_id'] = card.board_id
    return_dict = {
        "message": f"Card with id {card.id} successfully created in {board.title}",
        "card": card_dict
        }
    return jsonify(return_dict), 201

#------get card by id --------
@cards_bp.route("/<board_id>/cards/<card_id>",methods = ["GET"]) 
def get_card_by_id(card_id):
    try:
        id = int(card_id)
    except:
        abort(make_response({"message": f"{card_id} is not a valid id"}, 400))    
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
@cards_bp.route("/<board_id>/cards/<card_id>", methods=["DELETE"])
def remove_card_by_id(card_id):
    try:
        id = int(card_id)
    except:
        abort(make_response({"message": f"{card_id} is not a valid id"}, 400)) 
    card = Card.query.get(id)

    if (card == None):
        abort(make_response({"message":f"card {id} not found"}, 404))
    
    db.session.delete(card)
    db.session.commit()
    return jsonify({
        "message":f"Card {id} \"{card.message}\" successfully deleted"
        }, 200)
    
#------------update card by id---------
@cards_bp.route("/<board_id>/cards/<card_id>", methods=["PATCH"])
def update_card_by_id(card_id):
    try:
        id = int(card_id)
    except:
        abort(make_response({"message": f"{card_id} is not a valid id"}, 400))
    card = Card.query.get(id)

    if (card == None):
        abort(make_response({"message":f"card {id} not found"}, 404))
    update_dict = request.get_json()
    
    for k, v in update_dict.items():
        if k in {'message', 'likes_count'}:
            setattr(card, k, v)
    
    db.session.commit()

    card_dict={}
    card_dict['id'] = card.id
    card_dict['message'] = card.message
    card_dict['likes_count'] = card.likes_count
    
    return_dict = {
        "message": f"Card with id of {card.id} successfully updated",
        "card": card_dict
        }
    return jsonify(return_dict), 200

