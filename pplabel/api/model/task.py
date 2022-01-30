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
        db.Integer(), db.ForeignKey("project.project_id", ondelete="CASCADE")
    )
    project = db.relationship("Project")
    datas = db.relationship("Data", backref="task", lazy="selectin")
    annotations = db.relationship("Annotation", backref="task", lazy="selectin")
