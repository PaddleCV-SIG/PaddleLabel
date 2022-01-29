from datetime import datetime

from pplabel.config import db
from pplabel.api.util import nncol

# TODO: circular risk
from ..setting import TaskCategory


class Project(db.Model):
    __tablename__ = "project"
    __table_args__ = {"comment": "Stores information and settings for each project"}
    project_id = nncol(db.Integer, primary_key=True)
    name = nncol(db.String(), unique=True)
    description = db.Column(db.String())
    task_category_id = db.Column(
        db.Integer(), db.ForeignKey("taskCategory.task_category_id")
    )  # TODO: smallint
    task_category = db.relationship("TaskCategory")
    data_dir = nncol(db.String(), unique=True)
    label_dir = db.Column(db.String(), unique=True)
    labels = db.relationship("Label")
    created = nncol(db.DateTime, default=datetime.utcnow)
    modified = nncol(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    other_settings = db.Column(db.String())

    to_json = ["label_config"]

    def __repr__(self):
        s = f"--------------------\n{self.__tablename__}\n"
        for att in dir(self):
            if att[0] != "_":
                s += f"{att}: {getattr(self, att)}\n"
        s += "--------------------\n"
        return s

    def _get_task_category(self):
        task_category = TaskCategory.query.filter(
            TaskCategory.task_category_id == self.task_category_id
        ).one()
        print("}}}}}}}}}}}}}}}}}}}", task_category)
        return task_category
