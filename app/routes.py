import requests
import os
from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board
from app.models.board import Card

# # example_bp = Blueprint('example_bp', __name__)

# # Boards Routes

# boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

# # POST /boards
# @boards_bp.route("", methods=["POST"])

# # GET /boards/<board_id>
# @boards_bp.route("/<board_id>", methods=["GET"])

# # PUT /boards/<board_id> ??? Do we want ???
# @boards_bp.route("/<board_id>", methods=["PUT"])

# # ??? Do we want PATCH routes for title or owner ???

# # DELETE /boards/<board_id>
# @boards_bp.route("/<board_id>", methods=["DELETE"])

# # Cards Routes

# cards_bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

# # POST /cards
# @cards_bp.route("", methods=["POST"])

# # GET /cards
# @cards_bp.route("", methods=["GET"])

# # PUT /cards/<card_id>/ ??? Do we want ???

# # PATCH /cards/<card_id>/likes_count
# @cards_bp.route("/<card_id>/likes_count", methods=["PATCH"])

# # ??? Do we want PATCH route for message ???

# # DELETE /cards/<card_id>
# @cards_bp.route("/<card_id>", methods=["DELETE"])
