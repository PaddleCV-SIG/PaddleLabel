import json

from flask import make_response, abort, request
import sqlalchemy

from pplabel.config import db
from .model import immutable_properties


def get_all(Model, Schema):
    items = Model.query.all()
    return Schema(many=True).dump(items), 200


def get(Model, Schema, **kwargs):
    id_name, id_val = list(kwargs.items())[0]
    item = Model.query.filter(getattr(Model, id_name) == id_val).one_or_none()

    if item is not None:
        return Schema().dump(item)
    abort(404, f"No {id_name.split('_')[0]} with id: {id_val}")


def post(Model, Schema, immutables=immutable_properties):
    schema = Schema()
    new_item = schema.load(request.get_json())
    try:
        db.session.add(new_item)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        msg = str(e.orig)
        if msg.startswith("UNIQUE constraint failed"):
            col = msg.split(":")[1].strip()
            abort(
                409,
                f"{Model.__tablename__} doesn't allow uplicate {col}.",
            )
        else:
            abort(500, msg)
    return schema.dump(new_item), 201


def put(Model, Schema, **kwargs):
    # 1. check project exists
    id_name, id_val = list(kwargs.items())[0]
    item = Model.query.filter(getattr(Model, id_name) == id_val).one_or_none()
    if item is None:
        abort(404, f"{Model.__tablename__.capitalize()} with {id_name} {id_val} is not found.")
    body = request.get_json()
    print("+_+_+", body)
    print(len(body.items()))
    if len(body.items()) == 1:
        # 2.1 key in keys: change one property
        k, v = list(body.items())[0]
        if k in immutable_properties:
            abort(403, f"{Model.__tablename__}.{k} doesn't allow edit")
        cols = [c.key for c in Model.__table__.columns]
        if k not in cols:
            abort(404, f"Project doesn't have property {k}")
        setattr(item, k, v)
        db.session.commit()
    else:
        # 2.2 change all provided properties
        Model.query.filter(getattr(Model, id_name) == id_val).update(body)
        db.session.commit()

    # FIXME: really need to requery?
    item = Model.query.filter(getattr(Model, id_name) == id_val).one_or_none()
    return Schema().dump(item), 200


def delete(Model, Schema, **kwargs):
    id_name, id_val = list(kwargs.items())[0]
    item = Model.query.filter(getattr(Model, id_name) == id_val).one_or_none()

    if item is None:
        abort(404, f"No {Model.__tablename__} with {id_name} == {id_val}")
        pass

    db.session.delete(item)
    db.session.commit()
    return f"{Model.__tablename__.capitalize()} {id_val} deleted", 200


def crud(Model, Schema, immutables=immutable_properties):
    get_all = functools.partial(get_all, Project, ProjectSchema)
    get = functools.partial(get, Project, ProjectSchema)
    post = functools.partial(post, Project, ProjectSchema)
    put = functools.partial(put, Project, ProjectSchema, immutables)
    delete = functools.partial(delete, Project, ProjectSchema)
    return get_all, get, post, put, delete
