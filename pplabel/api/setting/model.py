import os.path as osp

from functools import total_ordering

from pplabel.config import db
from pplabel.api.util import nncol


class TaskCategory(db.Model):
    __tablename__ = "taskCategory"
    task_category_id = nncol(
        db.Integer(),
        primary_key=True,
        autoincrement=False,
    )
    name = nncol(db.String(), unique=True)
    handler = db.Column(db.String(), unique=True)
    # print("XXXXXXXXXXXXXXXXX visited TaskCategory")

    def __init__(self, task_category_id, name, handler):
        super().__init__()
        self.task_category_id = task_category_id
        self.name = name
        if len(handler) == 0:
            self.handler = None
        else:
            self.handler = handler

    def __repr__(self):
        return f"name: {self.name}, task_category_id: {self.task_category_id}, handler: {self.handler}"
