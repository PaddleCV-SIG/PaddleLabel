from datetime import datetime

from pplabel.config import db
from pplabel.api.util import nncol


class Task(db.Model):
    __tablename__ = "task"
    __table_args__ = {"comment": "Contains all the tasks"}
    task_id = nncol(db.Integer(), primary_key=True)
    project_id = nncol(db.Integer(), db.ForeignKey("project.project_id"))
    data_paths = nncol(db.String())
    slice_count = nncol(db.Integer())
    created = nncol(db.DateTime, default=datetime.utcnow)
    modified = nncol(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
