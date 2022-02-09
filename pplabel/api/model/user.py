from datetime import datetime

from pplabel.config import db
from pplabel.api.util import nncol

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "user"
    __table_args__ = {"comment": "Stores all user info"}
    user_id = nncol(db.Integer, primary_key=True)
    name = nncol(db.String(), unique=True)
    email = nncol(db.String())
    password = nncol(db.String())
    role_id = nncol(db.Integer())

    _immutables = BaseModel._immutables + ["user_id"]
