from datetime import datetime

from sqlalchemy.orm import backref

from pplabel.config import db
from ..util import nncol
from .annotation import Annotation
from .project import Project
from .base import BaseModel


class Task(BaseModel):
    __tablename__ = "task"
    __table_args__ = {"comment": "Contains all the tasks"}
    task_id = nncol(db.Integer(), primary_key=True)
    project_id = nncol(
        db.Integer(),
        db.ForeignKey("project.project_id", ondelete="CASCADE"),
    )
    datas = db.relationship("Data", lazy="selectin", cascade="all, delete-orphan")
    annotations = db.relationship("Annotation", lazy="selectin", cascade="all, delete-orphan")
    set = nncol(db.Integer())
