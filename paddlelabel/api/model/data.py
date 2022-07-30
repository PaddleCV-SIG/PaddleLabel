from datetime import datetime

from paddlelabel.config import db
from ..util import nncol
from .base import BaseModel


class Data(BaseModel):
    __tablename__ = "data"
    __table_args__ = {"comment": "Contains all the data files"}
    data_id = nncol(db.Integer(), primary_key=True)
    task_id = db.Column(db.Integer(), db.ForeignKey("task.task_id", ondelete="CASCADE"))
    # task = db.relationship("Task", lazy="selectin")
    annotations = db.relationship("Annotation", lazy="selectin", cascade="all, delete-orphan")
    path = nncol(db.String())
    size = db.Column(db.String())  # , seperated string. natural image: NHWC (C is optional)

    _immutables = BaseModel._immutables + ["data_id", "task_id"]
