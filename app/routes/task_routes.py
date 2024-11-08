from .route_utilities import create_model, validate_model, get_models_with_filters, wrapper, slack_post, update_model
from flask import Blueprint, make_response, abort, request, Response
from app.models.task import Task
from datetime import datetime
from ..db import db

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)


@bp.get("")
def get_all_tasks():
    return get_models_with_filters(Task, request.args)


@bp.get("/<id>")
def get_single_task(id):
    task = validate_model(Task, id)

    return wrapper(task)
@bp.put("/<id>")
def update_task(id):
    task = validate_model(Task, id)
    request_body = request.get_json()

    return update_model(task, request_body)

@bp.delete("/<id>")
def delete_task(id):
    task = validate_model(Task, id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f"Task {task.id} \"{task.title}\" successfully deleted"}

@bp.patch("/<id>/mark_complete")
def mark_task_complete(id):
    task: Task = validate_model(Task, id)

    task.completed_at = datetime.utcnow()
    
    db.session.commit()

    slack_post(task.title)

    return wrapper(task)

@bp.patch("/<id>/mark_incomplete")
def mark_task_incomplete(id):
    task: Task = validate_model(Task, id)

    task.completed_at = None
    
    db.session.commit()

    return wrapper(task), 200







