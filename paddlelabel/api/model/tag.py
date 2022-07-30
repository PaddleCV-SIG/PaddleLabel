from paddlelabel.config import db
from paddlelabel.api.util import nncol
from .base import BaseModel


class Tag(BaseModel):
    __tablename__ = "tag"
    __table_args__ = {"comment": "Contains all the tags"}
    tag_id = nncol(db.Integer(), primary_key=True)
    project_id = nncol(db.Integer(), db.ForeignKey("project.project_id"))
    name = nncol(db.String())
    color = db.Column(db.String())
    comment = db.Column(db.String())

    _immutables = BaseModel._immutables + ["tag_id", "project_id"]
