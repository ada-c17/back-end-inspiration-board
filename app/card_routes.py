from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from app.models.board import Board

# example_bp = Blueprint('example_bp', __name__)
cards_bp = Blueprint("cards", __name__, url_prefix="/boards/<board_id>/cards")


@cards_bp.route("", methods = ["GET"])
def get_all_cards():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        cards = Card.query.order_by(asc(Card.title))
    elif sort_query == "desc":
        cards = Card.query.order_by(desc(Card.title))
    else:
        cards = Card.query.all()
        
    return jsonify([card.to_dict_card() for card in cards]), 200




# creating card with using POST in our route decorator
@cards_bp.route("", methods = ["POST"])
def create_card(board_id): 
    request_body = request.get_json()
    if "message" not in request_body :
        return jsonify({"details": "Please provide message"}), 400
    elif len(request_body["message"]) < 40:
        return jsonify({"Invalid length : input must be under 40 character"}), 400
    
    new_card = Card(message= request_body["message"],
                    likes_count = request_body["likes_count"])
    board = Board.query.get(board_id)
    if board is None:
        return jsonify(""), 404  

    db.session.add(new_card)
    board.cards.append(card)
    db.session.commit()
    card = Card.query.order_by(Card.card_id.desc()).first()
    return make_response(jsonify({"card":new_card.to_dict_card()})), 201



