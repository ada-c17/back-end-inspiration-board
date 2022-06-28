from flask import Blueprint, request, jsonify, make_response
from app import db
# import models:
from .models.board import Board

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint("board_bp", __name__, url_prefix="/boards")

# Board Model routes:

# 1. POST - Create a new board, by filling out a form. The form includes "title" and "owner" name of the board.
# POST displays ERROR msg if empty/blank/invalid/missing "title" or "owner" input.


@board_bp.route("", methods=["POST"])
# 2.GET- Read; View a list of all boards
# 3. GET - Read; Select a specific board
