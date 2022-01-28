import json
import functools
from collections import defaultdict

from flask import make_response, abort, request
import sqlalchemy

from pplabel.config import db
from .model import immutable_properties


def crud(Model, Schema, immutables=immutable_properties, triggers=[]):
    tgs = defaultdict(lambda: None)
    for trigger in triggers:
        tgs[trigger.__name__] = trigger

    def get_all(
        Model,
        Schema,
        pre_get_all=tgs["pre_get_all"],
        post_get_all=tgs["post_get_all"],
    ):
        items = Model.query.order_by(getattr(Model, "modified")).all()
        if post_get_all is not None:
            post_get_all(items, db.session)
        return Schema(many=True).dump(items), 200

    def get(Model, Schema, **kwargs):
        id_name, id_val = list(kwargs.items())[0]
        item = Model.query.filter(getattr(Model, id_name) == id_val).one_or_none()

        if item is not None:
            return Schema().dump(item)
        abort(404, f"No {id_name.split('_')[0]} with id: {id_val}")

    def post(
        Model,
        Schema,
        pre_add=tgs["pre_add"],
        post_add=tgs["post_add"],
        immutables=immutable_properties,
    ):
        schema = Schema()
        new_item = schema.load(request.get_json())
        if pre_add is not None:
            pre_add(new_item, db.session)
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

        if post_add is not None:
            with db.session.no_autoflush:
                post_add(new_item, db.session)

        return schema.dump(new_item), 201

    def put(
        Model,
        Schema,
        immutables=immutable_properties,
        pre_put=tgs["pre_put"],
        post_put=tgs["post_put"],
        **kwargs,
    ):
        # 1. check project existgs
        id_name, id_val = list(kwargs.items())[0]
        item = Model.query.filter(getattr(Model, id_name) == id_val).one_or_none()
        if item is None:
            abort(
                404,
                f"{Model.__tablename__.capitalize()} with {id_name} {id_val} is not found.",
            )
        if pre_put is not None:
            pre_put(item, db.session)
        body = request.get_json()
        if len(body.items()) == 1:
            # 2.1 key in keys: change one property
            k, v = list(body.items())[0]
            if k in immutables:
                abort(403, f"{Model.__tablename__}.{k} doesn't allow edit")
            cols = [c.key for c in Model.__table__.columns]
            if k not in cols:
                abort(404, f"Project doesn't have property {k}")
            setattr(item, k, v)
            db.session.commit()
        else:
            # 2.2 change all provided properties
            for k in body.keys():
                if k in immutables:
                    abort(403, f"{Model.__tablename__}.{k} doesn't allow edit")
            Model.query.filter(getattr(Model, id_name) == id_val).update(body)
            db.session.commit()

        # FIXME: really need to requery?
        item = Model.query.filter(getattr(Model, id_name) == id_val).one_or_none()
        print("_______", post_put)
        if post_put is not None:
            post_put(item, db.session)
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

    get_all = functools.partial(get_all, Model, Schema)
    get = functools.partial(get, Model, Schema)
    post = functools.partial(post, Model, Schema)
    put = functools.partial(put, Model, Schema, immutables)
    delete = functools.partial(delete, Model, Schema)
    return get_all, get, post, put, delete
