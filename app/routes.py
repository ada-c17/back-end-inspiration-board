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

    return_dict = {
        "message": f"Board with id of {board.id} successfully created",
        "board": board.as_dict()
        }
    return jsonify(return_dict), 201

#------------GET ALL BOARDS---------------
@boards_bp.route("", methods=["GET"]) 
def get_all_boards():
    board_db = Board.query.all()  

    boards_response = [] 
    for board in board_db:             
        boards_response.append(board.as_dict())
    return jsonify({"boards": boards_response}), 200  

#-----------------------------------
@boards_bp.route("/<id>", methods=["GET"]) 
def get_board_by_id(id):
    board = Board.validate_and_get_by_id(id)

    return_dict = {"board": board.as_dict()}
    return jsonify(return_dict), 200

#------------Update board details---------
@boards_bp.route("/<id>", methods=["PATCH"])
def update_board_by_id(id):
    board = Board.validate_and_get_by_id(id)

    update_dict = request.get_json()

    for k, v in update_dict.items():
        if k in {'title', 'owner'}:
            setattr(board, k, v)
    
    db.session.commit()
    
    return_dict = {
        "message": f"Board with id of {board.id} successfully updated",
        "board": board.as_dict()
        }
    return jsonify(return_dict), 200

#------------remove board by id------------
@boards_bp.route("/<id>", methods=["DELETE"])
def remove_board_by_id(id):
    board = Board.validate_and_get_by_id(id)
    
    db.session.delete(board)
    db.session.commit()
    return jsonify({
        "message": f"Board {id} \"{board.title}\" successfully deleted"
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
    
    board = Board.validate_and_get_by_id(id)

    card = Card(message = message, likes_count = 0, board_id = board.id)

    db.session.add(card)
    db.session.commit()

    return_dict = {
        "message": f"Card with id {card.id} successfully created in {board.title}",
        "card": card.as_dict()
        }
    return jsonify(return_dict), 201

#------get card by id --------
@cards_bp.route("/<board_id>/cards/<card_id>",methods = ["GET"]) 
def get_card_by_id(card_id):
    card = Card.validate_and_get_by_id(card_id)
    return_dict = {"card": card.as_dict()}
    return jsonify(return_dict), 200

#------------remove card by id------------
@cards_bp.route("/<board_id>/cards/<card_id>", methods=["DELETE"])
def remove_card_by_id(card_id):
    card = Card.validate_and_get_by_id(card_id)
    
    db.session.delete(card)
    db.session.commit()

    return jsonify({
        "message":f"Card {id} \"{card.message}\" successfully deleted"
        }, 200)
    
#------------update card by id---------
@cards_bp.route("/<board_id>/cards/<card_id>", methods=["PATCH"])
def update_card_by_id(card_id):
    card = Card.validate_and_get_by_id(card_id)
    update_dict = request.get_json()
    
    for k, v in update_dict.items():
        if k in {'message', 'likes_count'}:
            setattr(card, k, v)
    
    db.session.commit()
    
    return_dict = {
        "message": f"Card with id of {card.id} successfully updated",
        "card": card.as_dict()
        }
    return jsonify(return_dict), 200
