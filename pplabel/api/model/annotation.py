from datetime import datetime

from pplabel.config import db
from pplabel.api.util import nncol
from .base import BaseModel


class Annotation(BaseModel):
    __tablename__ = "annotation"
    __table_args__ = {"comment": "Contains all the annotations"}
    annotation_id = nncol(db.Integer(), primary_key=True)
    frontend_id = nncol(db.Integer())
    task_id = nncol(db.Integer(), db.ForeignKey("task.task_id", ondelete="CASCADE"))
    task = db.relationship("Task")
    project_id = nncol(db.Integer(), db.ForeignKey("project.project_id"))
    data_id = db.Column(db.Integer(), db.ForeignKey("data.data_id", ondelete="CASCADE"))
    result = db.Column(db.String())
    label_id = nncol(db.Integer(), db.ForeignKey("label.label_id", ondelete="CASCADE"))
    label = db.relationship("Label")
    type = db.Column(db.String())

    # task = db.relationship("Task")

    _immutables = BaseModel._immutables + ["annotation_id", "task_id", "slice_id"]
