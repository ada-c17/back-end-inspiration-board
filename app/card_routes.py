from app import db
from app.models.card import Card
from flask import Blueprint, jsonify, abort, make_response, request
# from .helper import validate_record, send_message_to_slack
from sqlalchemy import asc, desc
from datetime import datetime
from dotenv import load_dotenv

cards_bp = Blueprint("cards_bp", __name__, url_prefix="/cards")
load_dotenv()

def validate_record(cls, id):
    try:
        id = int(id)
    except ValueError:
        abort(make_response({"message": f"{cls} {id} is invalid"}, 400))

    obj = cls.query.get(id)

    if not obj:
        return abort(make_response({"message": f"{cls.__name__} {id} not found"}, 404))

    return obj

# CREATE card
@cards_bp.route("boards/<board_id>/cards", methods=["POST"])
def create_card():
    request_body = request.get_json()
    
    try:
        new_card = Card.create_complete(request_body)
    except KeyError:
        return abort(make_response(jsonify({"details":"Invalid data"}), 400))

    db.session.add(new_card)
    db.session.commit()

    return jsonify({'card': new_card.to_json()}), 201


# Get all cards of one board
# @goals_bp.route("/<goal_id>/tasks", methods=["GET"])
# def read_tasks_of_one_goal(goal_id):
#     goal = validate_record(Goal, goal_id)
#     tasks_response = [task.to_json() for task in goal.tasks]

#     response_body = {
#         "id": goal.goal_id,
#         "title": goal.title,
#         "tasks": tasks_response
#     }
    
#     return jsonify(response_body), 200



# # GET ALL cards of one board
# @cards_bp.route("boards/<board_id>/cards", methods=["GET"])
# def read_all_cards_one_board():
    

#     tasks_response = [task.to_json() for task in tasks]

#     return jsonify(tasks_response), 200

# GET one task
# @tasks_bp.route("/<task_id>", methods=["GET"])  
# def read_one_task(task_id):
#     task = validate_record(Task, task_id)
#     return jsonify({"task": task.to_json()}), 200

# UPDATE one card
@cards_bp.route("/cards/<card_id>/like", methods=["PUT"])
def update_card(card_id):
    card = validate_record(Card, card_id)
    request_body = request.get_json()

    try:
        card.update(request_body)
    except KeyError:
        return abort(make_response(jsonify({"details":"Invalid data"}), 400))

    db.session.commit()

    return jsonify({'card': card.to_json()}), 200
    

# DELETE one card
@card_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_record(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return jsonify({"details":f'Task {task.task_id} "{task.title}" successfully deleted'}), 200


# Mark task as complete
# @tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
# def mark_complete(task_id):
#     task = validate_record(Task, task_id)
#     task.completed_at = datetime.today()
#     db.session.commit()

#     send_message_to_slack(task)

#     return jsonify({'task': task.to_json()}), 200


# Mark task as incomplete
# @tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
# def mark_incomplete(task_id):
#     task = validate_record(Task, task_id)

#     task.completed_at = None

#     db.session.commit()

#     return jsonify({'task': task.to_json()}), 200