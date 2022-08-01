from paddlelabel.config import db
from paddlelabel.api.util import nncol
from .base import BaseModel


class TagTask(BaseModel):
    __tablename__ = "tagTask"
    __table_args__ = {"comment": "Tag and task intersect"}
    tag_task_id = nncol(db.Integer(), primary_key=True)
    project_id = nncol(db.Integer(), db.ForeignKey("project.project_id"))
    tag_id = nncol(db.Integer(), db.ForeignKey("tag.tag_id"))
    task_id = nncol(db.Integer(), db.ForeignKey("task.task_id"))
    tag = db.relationship("Tag")

    _immutables = BaseModel._immutables + [
        "tag_task_id",
        "project_id",
        "tag_id",
        "task_id",
    ]
