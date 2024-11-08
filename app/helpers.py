from flask import make_response, abort
from .db import db


def validate_model(cls, id):
    try:
        id = int(id)
    except:
        