from datetime import datetime

from sqlalchemy import event

from pplabel.config import db
from pplabel.api.util import nncol
from ..base import BaseModel


class Annotation(BaseModel):
    __tablename__ = "annotation"
    __table_args__ = {"comment": "Contains all the annotations"}
    annotation_id = nncol(db.Integer(), primary_key=True)
    task_id = db.Column(db.Integer(), db.ForeignKey("task.task_id", ondelete="CASCADE"))
    result = nncol(db.String())
    slice_id = nncol(db.Integer())

    _immutables = BaseModel._immutables + ["annotation_id", "task_id", "slice_id"]
