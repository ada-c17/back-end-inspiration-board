from flask import Blueprint, request, jsonify, make_response
from app import db

card_bp = Blueprint("card_bp", __name__, url_prefix="/cards")

# GET /boards/<board_id>/cards

# POST /boards/<board_id>/cards

# DELETE /cards/<card_id>

# PUT /cards/<card_id>/like
