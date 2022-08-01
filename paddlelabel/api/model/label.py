from datetime import datetime

from paddlelabel.config import db
from ..util import nncol
from .base import BaseModel


class Label(BaseModel):
    __tablename__ = "label"
    __table_args__ = {"comment": "Contains all the label information"}
    label_id = nncol(db.Integer(), primary_key=True)
    id = nncol(db.Integer())
    project_id = db.Column(db.Integer(), db.ForeignKey("project.project_id"))  # TODO: why missing project_id when nncol
    name = nncol(db.String())
    color = db.Column(db.String())
    comment = db.Column(db.String())
    annotations = db.relationship("Annotation", lazy="noload", backref="label")  # cascade="all, delete-orphan"
    super_category_id = db.Column(db.Integer())  # TODO: foreign key
    _immutables = BaseModel._immutables + ["label_id", "project_id"]
