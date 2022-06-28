from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.board import Board

board_bp = Blueprint('Boards', __name__, url_prefix='/boards')
