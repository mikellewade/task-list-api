from flask import abort, make_response
from sqlalchemy import asc, desc
from ..db import db
import requests
import os

def wrapper(model):
    return {f"{model.__class__.__name__.lower()}": model.to_dict()}

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} id {(model_id)} invalid"}, 400))
    
    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        abort(make_response({ "message": f"{cls.__name__} {model_id} not found"}, 404))
    
    return model

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    
    except KeyError as error:
        response = {"details": f"Invalid data"}
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()

    return wrapper(new_model), 201

def get_models_with_filters(cls, filters=None):
    query = db.select(cls)

    if filters:
        for attribute, value in filters.items():
            if hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))

    sort_param = filters.get("sort")
    sort = None

    match sort_param:
        case "asc":
            sort = asc(cls.title)
        case "desc":
            sort = desc(cls.title)
        case None:
            sort = cls.title

    models = db.session.scalars(query.order_by(sort))
    models_response = [model.to_dict() for model in models]

    return models_response

def slack_post(title):
    url = "https://slack.com/api/chat.postMessage"
    body = {
        "channel": "dev",
        "text": f"Task \"{title}\" was completed."
    }
    token = os.environ.get("SLACK_API_TOKEN")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }

    requests.post(url=url,data=body, headers=headers)

def update_model(model, updates):
    for attribute, value in updates.items():
            if hasattr(model, attribute):
                setattr(model, attribute, value)
    
    db.session.commit()

    return wrapper(model)
