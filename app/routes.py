from app.models.card import *
from app.models.board import *
from flask import Blueprint, request, jsonify, make_response, jsonify, abort
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# from app import db

# example_bp = Blueprint('example_bp', __name__)
cards_bp = Blueprint("cards_bp", __name__, url_prefix="/cards")
#-----post_card------

@cards_bp.route("", methods=["POST"])
def post_card():
    post_dict = request.get_json()
    if 'message' not in post_dict or 'likes_count' not in post_dict:
        return make_response({"details":"invalid data"},400)
    
    message = post_dict['message']
    likes_count = post_dict['likes_count']

    card = Card(message = message, likes_count = likes_count)
    db.session.add(card)
    db.session.commit()

    card_dict = {}
    card_dict['card_id'] = card.card_id
    card_dict['message'] = card.message
    card_dict['likes_count'] = card.likes_count
    return_dict = {"card": card_dict}
    return jsonify(return_dict),201

#--------get all tasks------------

@cards_bp.route("", methods=["GET"]) 
def get_all_cards():
    
    card_db = Card.query.all()
    
    cards_response = []
    for card in card_db:    
        card_dict = {'card_id': card.card_id,
                    'message': card.message,
                    'likes_count': card.likes_count}
                
        cards_response.append(card_dict)

    return jsonify(cards_response), 200    

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
    
    if card.board_id != None:
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

