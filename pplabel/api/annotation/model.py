from datetime import datetime

from sqlalchemy import event

from pplabel.config import db
from pplabel.api.util import nncol


class Annotation(db.Model):
    __tablename__ = "annotation"
    __table_args__ = {"comment": "Contains all the annotations"}
    annotation_id = nncol(db.Integer(), primary_key=True)
    task_id = db.Column(db.Integer(), db.ForeignKey("task.task_id", ondelete="CASCADE"))
    # task = db.relationship("Task", lazy="select")
    result = nncol(db.String())
    slice_id = nncol(db.Integer())
    created = nncol(db.DateTime, default=datetime.utcnow)
    modified = nncol(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
