from flask import Blueprint, request, jsonify, make_response
from app import db

board_bp = Blueprint("board_bp", __name__, url_prefix="/boards")

# GET /boards

# POST /boards
