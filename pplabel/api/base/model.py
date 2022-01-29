from datetime import datetime

from pplabel.config import db
from pplabel.api.util import nncol


class BaseModel(db.Model):
    __abstract__ = True
    __tablename__ = ""
    __table_args__ = {"comment": ""}
    created = nncol(db.DateTime, default=datetime.utcnow)
    modified = nncol(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    immutables = ["created", "modified", "immutables"]

    def __repr__(self):
        s = f"Object: {self.__tablename__}\n"
        for att in dir(self):
            if att[0] != "_":
                s += f"{att}: {getattr(self, att)}  "
        s += "\n"
        return s
