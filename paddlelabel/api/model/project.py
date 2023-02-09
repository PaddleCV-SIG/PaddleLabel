# -*- coding: utf-8 -*-
import json

from paddlelabel.config import db
from paddlelabel.api.util import nncol

# TODO: circular risk
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
    labels = db.relationship(
        "Label",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    tasks = db.relationship("Task", lazy="noload", cascade="all, delete-orphan")
    annotations = db.relationship("Annotation", lazy="noload", cascade="all, delete-orphan")
    other_settings = db.Column(db.String())

    label_format = db.Column(db.String())  # TODO: remove
    label_dir = db.Column(db.String())  # TODO: remove

    _immutables = BaseModel._immutables + ["project_id", "task_category_id"]

    def _get_other_settings(self):
        if self.other_settings is None:
            return {}
        print("asdf", type(json.loads(self.other_settings)), self.other_settings)
        return json.loads(self.other_settings)
