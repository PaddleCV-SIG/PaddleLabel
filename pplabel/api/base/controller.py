import json

from flask import make_response, abort, request
import sqlalchemy

from pplabel.config import db


def get_all(Model, Schema):
    items = Model.query.all()
    return Schema(many=True).dump(items), 200


def get(Model, Schema, **kwargs):
    id_name, id_val = list(kwargs.items())[0]
    print(kwargs, dir(Model))
    item = Model.query.filter(getattr(Model, id_name) == id_val).one_or_none()

    if item is not None:
        return Schema().dump(item)
    abort(404, f"No {id_name.split('_')[0]} with id: {id_val}")
