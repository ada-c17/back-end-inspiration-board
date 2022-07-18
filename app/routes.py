from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board 
from app.models.card import Card 


def validate_or_abort(board_id):
    # returns 400 error if invalid board_id (alpha/non-int) 
    try:
        board_id = int(board_id)
    except ValueError:
        abort(make_response({"error": f"{board_id} is an invalid board id"}, 400))
    
    # returns 404 error if board_id not found in database
    board = Board.query.get(board_id)
    if not board:
        abort(make_response({"error": f"Board {board_id} not found"}, 404))
    return board


boards_bp = Blueprint('boards_bp', __name__, url_prefix='/boards')

@boards_bp.route('', methods=['GET'])
def read_all_boards():
    '''
    GET method to /boards endpoint
    Returns: JSON body with id, title, and owner from all boards
    '''
    # board_query = request.args.get("sort")
    boards = Board.query.all()
    board_response = []
    for board in boards:
        board_response.append(
            {
                "id": board.board_id,
                "title": board.title,
                "owner": board.owner,
            }
        )
    return jsonify(board_response)

@boards_bp.route('', methods=['POST'])
def create_board():
    '''
    POST method to /boards endpoint
    Input: title and owner which are both required
    Returns: JSON response body with all input including id
    '''
    request_body = request.get_json()
    try:
        new_board = Board(
            title=request_body['title'], 
            owner=request_body['owner']
            )
    except:
        abort(make_response({'details': f'Invalid data'}, 400))
        
    db.session.add(new_board)
    db.session.commit()
    
    return {
        "id": new_board.board_id,
        "owner": new_board.owner,
        "title": new_board.title,
    }, 201

@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    '''
    DELETE method to boards/<board_id> endpoint
    Input: sending a board with a specific id will delete that board
    Returns: success message with specific board id and board title 
    '''
    board = validate_or_abort(board_id)

    db.session.delete(board)
    db.session.commit()

    return jsonify({"details": f"Board {board_id} \"{board.title}\" successfully deleted"}), 200

@boards_bp.route("/<board_id>", methods=["GET"]) 
def read_cards_for_one_board(board_id): 
    '''
    GET method to /boards/<board_id>/cards endpoint
    Returns: JSON body with id, message, and like_count of all cards for the specific board
    '''
    board = validate_or_abort(board_id)
    cards = Card.query.all()
    cards_response = []
    for card in cards:
        if card.board_id == board.board_id: 
            cards_response.append(
                { 
                "card_id": card.card_id, 
                "message": card.message, 
                "likes_count": card.likes_count,
                "board_id": card.board_id
                }
            )
    return jsonify(cards_response)

@boards_bp.route("/<board_id>/cards", methods=["POST"])
def create_cards_for_one_board(board_id): 
    '''
    POST method to /boards/<board_id>/cards endpoint
    Input: message, like_count, and board title which are all required
    Returns: JSON response body with all input including id and successfully created message
    '''
    board = validate_or_abort(board_id)

    request_body = request.get_json()
    new_card = Card(
        message=request_body["message"], 
        like_count=request_body["like_count"], 
        board=board.title 
    )

    db.session.add(new_card)
    db.session.commit()

    return make_response(jsonify(f"Card {new_card.message} in {board.title} successfully created"), 201)


