from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
from app.models.board import Board 


cards_bp = Blueprint("cards", __name__, url_prefix="/cards")


# example_bp = Blueprint('example_bp', __name__)
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# @cards_bp.route("/<card_id>", methods=["DELETE"])
# def delete_card_by_id(card_id):
