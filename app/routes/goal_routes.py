from .route_utilities import get_models_with_filters, wrapper, validate_model, create_model, update_model
from flask import Blueprint, request
from ..models.goal import Goal
from ..models.task import Task
from ..db import db

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)

@bp.get("")
def get_goals():
    return get_models_with_filters(Goal, request.args)

@bp.get("/<id>")
def get_single_goal(id):
    goal = validate_model(Goal, id)

    return wrapper(goal)

@bp.put("/<id>")
def update_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json

    return update_model(goal, request_body)

@bp.delete("/<id>")
def delete_goal(id):
    goal = validate_model(Goal, id)

    db.session.delete(goal)
    db.session.commit()

    return {
  "details": f"Goal 1 \"{goal.title}\" successfully deleted"
}

@bp.post("/<id>/tasks")
def create_tasks_by_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()
    task_ids = request_body.get("task_ids")

    if task_ids:

        for task_id in task_ids:
            task = validate_model(Task, task_id)
            task.goal_id = goal.id

    db.session.commit()
    print(task_ids)

    return {
        "id": goal.id,
        "task_ids": task_ids if task_ids else []
    }

@bp.get("/<id>/tasks")
def get_task_by_id(id):
    goal = validate_model(Goal, id)
    tasks_list = [task.to_dict() for task in goal.tasks]

    goal_dict = goal.to_dict()
    goal_dict["tasks"] = tasks_list

    return goal_dict
