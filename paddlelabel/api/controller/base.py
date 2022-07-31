import functools
from collections import defaultdict


import connexion
from flask import abort  # TODO: change to connextion abort
import sqlalchemy
import marshmallow

from paddlelabel.config import db
from paddlelabel.api.util import parse_order_by

# TODO: implement a search method
def crud(Model, Schema, triggers=[]):
    tgs = defaultdict(lambda: None)
    for trigger in triggers:
        tgs[trigger.__name__] = trigger

    def get_all(
        Model,
        Schema,
        order_by="modified desc",
        pre_get_all=tgs["pre_get_all"],
        post_get_all=tgs["post_get_all"],
    ):
        order = parse_order_by(Model, order_by)

        items = Model.query.order_by(order).all()
        # print(items)
        if post_get_all is not None:
            post_get_all(items, db.session)
        return Schema(many=True).dump(items), 200

    def get(Model, Schema, **kwargs):
        id_name, id_val = list(kwargs.items())[0]
        item = Model.query.filter(getattr(Model, id_name) == id_val).one_or_none()

        if item is not None:
            return Schema().dump(item), 200
        abort(404, f"No {id_name.split('_')[0]} with id: {id_val}")

    def post(
        Model,
        Schema,
        pre_add=tgs["pre_add"],
        post_add=tgs["post_add"],
    ):
        schema = Schema()
        try:
            new_item = schema.load(connexion.request.json)
        except marshmallow.exceptions.ValidationError as e:
            for field, msgs in e.messages.items():
                if "Missing data for required field." in msgs:
                    # TODO: change code
                    abort(
                        500,
                        f"Marshmallow catch: Missing data for required field: {field}",
                    )
            abort(500, e.messages)
        if pre_add is not None:
            new_item = pre_add(new_item, db.session)
        try:
            db.session.add(new_item)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            msg = str(e.orig)
            if msg.startswith("UNIQUE constraint failed"):
                col = msg.split(":")[1].strip()
                abort(
                    409,
                    f"{Model.__tablename__} doesn't allow duplicate {col}.",
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
        pre_put=tgs["pre_put"],
        post_put=tgs["post_put"],
        **kwargs,
    ):
        # 1. check item exist
        id_name, id_val = list(kwargs.items())[0]
        item = Model.query.filter(getattr(Model, id_name) == id_val).one_or_none()
        if item is None:
            abort(
                404,
                f"No {Model.__tablename__} with {id_name}: {id_val} .",
            )
        # 2. check request key exist and can be edited
        body = connexion.request.json

        for k in list(body.keys()):
            if k in Model._immutables:
                # abort(403, f"{Model.__tablename__}.{k} doesn't allow edit")
                del body[k]
            if k not in Model._cols:
                abort(404, f"{Model.__tablename__}.{k} doesn't have property {k}")

        if pre_put is not None:
            item, body = pre_put(item, body, db.session)

        # 3. edit item
        Model.query.filter(getattr(Model, id_name) == id_val).update(body)
        db.session.commit()

        # FIXME: really need to requery?
        item = Model.query.filter(getattr(Model, id_name) == id_val).one()
        if post_put is not None:
            post_put(item, db.session)
        return Schema().dump(item), 200

    def delete(
        Model,
        Schema,
        pre_delete=tgs["pre_delete"],
        post_delete=tgs["post_delete"],
        **kwargs,
    ):
        id_name, id_val = list(kwargs.items())[0]
        item = Model.query.filter(getattr(Model, id_name) == id_val).one_or_none()

        if item is None:
            # abort(404, f"No {Model.__tablename__} with {id_name} == {id_val}")
            return

        if pre_delete is not None:
            item = pre_delete(item, db.session)
        db.session.delete(item)

        if post_delete is not None:
            post_delete(item, db.session)

        db.session.commit()

        return f"{Model.__tablename__.capitalize()} {id_val} deleted", 200

    get_all = functools.partial(get_all, Model, Schema)
    get = functools.partial(get, Model, Schema)
    post = functools.partial(post, Model, Schema)
    put = functools.partial(put, Model, Schema)
    delete = functools.partial(delete, Model, Schema)
    return get_all, get, post, put, delete
