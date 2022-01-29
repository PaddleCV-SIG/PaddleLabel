from datetime import datetime

from pplabel.serve import db
from pplabel.api.util import nncol


class Project(db.Model):
    __tablename__ = "project"
    __table_args__ = {"comment": "Stores information and settings for each project"}
    project_id = nncol(db.Integer, primary_key=True)
    name = nncol(db.String(), unique=True)
    description = db.Column(db.String())
    task_category = nncol(db.Integer())  # TODO: smallint
    data_dir = nncol(db.String(), unique=True)
    label_dir = db.Column(db.String(), unique=True)
    label_config = db.Column(db.String())
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

    # tasks = db.relationship(
    #     "Task",
    #     # backref="project",
    #     back_populates="project",
    #     cascade="all, delete, delete-orphan",
    #     single_parent=True,
    #     order_by="desc(Task.created)",
    #     lazy="noload",
    # )  # TODO: order by file name or slice
    # tasks = db.relationship(
    #     "Task",
    #     back_populates="project",
    #     # lazy="noload",
    #     lazy="noload",
    # )
