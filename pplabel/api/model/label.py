from datetime import datetime

from pplabel.config import db
from ..util import nncol
from .base import BaseModel


class Label(BaseModel):
    __tablename__ = "label"
    __table_args__ = {"comment": "Contains all the label information"}
    label_id = nncol(db.Integer(), primary_key=True)
    id = nncol(db.Integer())
    project_id = db.Column(
        db.Integer(), db.ForeignKey("project.project_id", ondelete="CASCADE")
    )
    name = nncol(db.String())
    color = db.Column(db.String())
    comment = db.Column(db.String())

    _immutables = BaseModel._immutables + ["label_id", "project_id"]
