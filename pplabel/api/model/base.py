from datetime import datetime

from pplabel.config import db
from pplabel.api.util import nncol
from ..util import abort

# TODO: nn string col cant be ""
class BaseModel(db.Model):
    __abstract__ = True
    __tablename__ = ""
    __table_args__ = {"comment": ""}
    created = nncol(db.DateTime, default=datetime.utcnow)
    modified = nncol(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    _immutables = ["created", "modified", "immutables"]

    @classmethod
    @property
    def _cols(cls):
        return [c.key for c in cls.__table__.columns]

    def __repr__(self):
        s = f"Object: {self.__tablename__}\n"
        for att in dir(self):
            if att[0] != "_":
                s += f"{att}: {getattr(self, att)}  "
        s += "\n"
        return s

    @classmethod
    def _exists(cls, item_id, throw=True):
        item = cls.query.filter(
            getattr(cls, cls.__tablename__ + "_id") == item_id
        ).one_or_none()
        if item is None:
            if throw:
                abort(f"No {cls.__tablename__} with id : {item_id}", 404)
            else:
                return False
        return True

    @classmethod
    def _get(cls, **kwargs):
        many = kwargs.get("many", False)
        if "many" in kwargs.keys():
            del kwargs["many"]
        for key in kwargs.keys():
            if key not in cls._cols:
                raise AttributeError(
                    f"Model {cls.__tablename__} don't have attribute {key}"
                )
        # TODO: none value

        conditions = {}
        for k, v in list(kwargs.items()):
            conditions[k] = v
        if many:
            items = cls.query.filter_by(**conditions).all()
            return items

        item = cls.query.filter_by(**conditions).one_or_none()
        return item

    @classmethod
    def _add(cls, item):
        db.session.add(item)
        db.session.commit()
