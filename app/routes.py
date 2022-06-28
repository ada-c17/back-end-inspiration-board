from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board 


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
def list_all_boards():
    board_query = request.args.get("sort")
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
    board = validate_or_abort(board_id)

    db.session.delete(board)
    db.session.commit()

    return jsonify({"details": f"Board {board_id} \"{board.title}\" successfully deleted"}), 200
