from datetime import datetime

from pplabel.config import db
from pplabel.api.util import nncol


class Project(db.Model):
    __tablename__ = "project"
    __table_args__ = {"comment": "Stores information and settings for each project"}
    project_id = nncol(db.Integer, primary_key=True)
    name = nncol(db.String(), unique=True)
    description = db.Column(db.String())
    task_category = nncol(db.SmallInteger())
    data_dir = nncol(db.String(), unique=True)
    label_dir = db.Column(db.String(), unique=True)
    label_config = db.Column(db.String())
    created = nncol(db.DateTime, default=datetime.utcnow)
    modified = nncol(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    other_settings = db.Column(db.String())

    tasks = db.relationship(
        "Task",
        backref="project",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Task.created)",
        lazy="noload",
    )  # TODO: order by file name or slice
