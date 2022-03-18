from datetime import datetime

from pplabel.config import db
from pplabel.api.util import nncol

# TODO: circular risk
from .setting import TaskCategory
from .base import BaseModel


class Project(BaseModel):
    __tablename__ = "project"
    __table_args__ = {"comment": "Stores information and settings for each project"}
    project_id = nncol(db.Integer, primary_key=True)
    name = nncol(db.String(), unique=True)
    description = db.Column(db.String())
    task_category_id = db.Column(db.Integer(), db.ForeignKey("taskCategory.task_category_id"))
    task_category = db.relationship("TaskCategory")
    data_dir = nncol(db.String(), unique=True)
    label_dir = db.Column(db.String(), unique=True)
    labels = db.relationship(
        "Label",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    tasks = db.relationship("Task", lazy="noload", cascade="all, delete-orphan")
    format = db.Column(db.String())
    other_settings = db.Column(db.String())

    _immutables = BaseModel._immutables + ["project_id", "task_category_id"]
