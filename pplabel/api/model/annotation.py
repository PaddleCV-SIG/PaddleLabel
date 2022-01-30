from datetime import datetime

from pplabel.config import db
from pplabel.api.util import nncol
from .base import BaseModel


class Annotation(BaseModel):
    __tablename__ = "annotation"
    __table_args__ = {"comment": "Contains all the annotations"}
    annotation_id = nncol(db.Integer(), primary_key=True)
    task_id = nncol(db.Integer(), db.ForeignKey("task.task_id", ondelete="CASCADE"))
    label_id = nncol(db.Integer(), db.ForeignKey("label.label_id"))
    project_id = nncol(db.Integer(), db.ForeignKey("project.project_id"))
    result = db.Column(db.String())
    slice_id = nncol(db.Integer())
    label = db.relationship("Label", lazy="noload")

    _immutables = BaseModel._immutables + ["annotation_id", "task_id", "slice_id"]
