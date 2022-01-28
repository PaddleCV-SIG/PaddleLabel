from datetime import datetime

from pplabel.config import db
from pplabel.api.util import nncol


class Data(db.Model):
    __tablename__ = "data"
    __table_args__ = {"comment": "Contains all the data files"}
    data_id = nncol(db.Integer(), primary_key=True)
    task_id = db.Column(db.Integer(), db.ForeignKey("task.task_id", ondelete="CASCADE"))
    path = nncol(db.String())
    slice_count = db.Column(db.Integer())
    created = nncol(db.DateTime, default=datetime.utcnow)
    modified = nncol(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    task = db.relationship("Task", lazy="select")
