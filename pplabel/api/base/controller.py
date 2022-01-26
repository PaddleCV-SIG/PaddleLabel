import json

from flask import make_response, abort, request
import sqlalchemy

from pplabel.config import db

def get_all(Model, Schema):
    items = Model.query.all()
    return Schema(many=True).dump(items), 200

def get(Model, Schema, id):
    print(dir(Model))
    item = Model.query.filter(Model.id == id).one_or_none()

    if item is not None:
        return Schema().dump(item)
    abort(404, f"Project not found for Id: {id}")
