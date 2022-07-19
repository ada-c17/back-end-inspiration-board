from email import message
from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card

cards_bp = Blueprint('cards_bp', __name__, url_prefix='/cards')

def validate_id_or_abort(card_id):
    # returns 400 error if invalid card_id (alpha/non-int) 
    try:
        card_id = int(card_id)
    except ValueError:
        abort(make_response({"error": f"{card_id} is an invalid card id"}, 400))
    
    # returns 404 error if card_id not found in database
    card = Card.query.get(card_id)
    if not card:
        abort(make_response({"error": f"card {card_id} not found"}, 404))
    return card


# This was our original GET route which is not currently needed. Current GET route for
# showing cards associated with a board is URL/boards/board_id

# @cards_bp.route('', methods=['GET'])
# def get_cards():
#     '''
#     GET method to /cards endpoint
#     Returns: JSON body with id, message, likes_count, and board_id from all cards
#     '''
#     card_query = request.args.get("sort") 
#     if card_query == "desc": 
#         cards = Card.query.order_by(Card.card_id.desc())
#     else:
#         cards = Card.query.order_by(Card.card_id.asc())
#     # else: 
#     #     Card.query.order_by(Card.id).all()
#     # cards = Card.query.all()
#     card_response = []
#     for card in cards:
#         card_response.append(
#             {
#                 "card_id": card.card_id,
#                 "message": card.message,
#                 "likes_count": card.likes_count,
#                 "board_id": card.board_id
#             }
#         )
#     return jsonify(card_response)

@cards_bp.route('', methods=['POST'])
def create_card():
    '''
    POST method to /cards endpoint
    Input: message, likes_count, and board_id which are all required
    Returns: JSON response body with all input including id
    '''
    request_body = request.get_json()
    try:
        new_card = Card(
            message=request_body['message'], 
            likes_count=request_body['likes_count'],
            board_id = request_body['board_id']
            )
    except:
        abort(make_response({'details': f'Invalid data'}, 400))
        
    db.session.add(new_card)
    db.session.commit()
    
    return {
        "card_id": new_card.card_id,
        "message": new_card.message,
        "likes_count": new_card.likes_count,
        "board_id": new_card.board_id
    }, 201

@cards_bp.route("/<card_id>/like", methods=["PUT"])
def update_card_likes(card_id):
    '''
    PUT method to cards/<card_id>/like endpoint
    Input: likes_count, which is required
    Returns: success message with specific card id
    '''
    card = validate_id_or_abort(card_id)
    request_body = request.get_json()

    if "likes_count" not in request_body:
        return jsonify({'msg': f"Request must include likes_count data"}), 400

    card.likes_count = request_body["likes_count"]
    
    # try:
    #     card.likes_count = request_body["likes_count"]
    # except KeyError:
    #     abort(make_response({'msg': f"Request must include likes_count data"}), 400)
    

    db.session.commit()

    return make_response(
        jsonify({'msg': f"Successfully updated likes of card with id {card_id}"}),
        200
    )

@cards_bp.route("/<card_id>", methods=['DELETE'])
def delete_card(card_id):
    '''
    DELETE method to cards/<card_id> endpoint
    Input: sending card with a specific id will delete that card
    Returns: success message with id of deleted card
    '''
    card= validate_id_or_abort(card_id)

    db.session.delete(card)
    db.session.commit()

    return {'details': f'Card {card.card_id} successfully deleted'}