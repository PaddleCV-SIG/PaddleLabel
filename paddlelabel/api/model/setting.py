import os.path as osp

from functools import total_ordering

from paddlelabel.config import db
from paddlelabel.api.util import nncol
from .base import BaseModel


class TaskCategory(BaseModel):
    __tablename__ = "taskCategory"
    task_category_id = nncol(
        db.Integer(),
        primary_key=True,
        autoincrement=False,
    )
    name = nncol(db.String(), unique=True)
    handler = db.Column(db.String())

    def __init__(self, task_category_id, name, handler):
        super().__init__()
        self.task_category_id = task_category_id
        self.name = name
        if len(handler) == 0:
            self.handler = None
        else:
            self.handler = handler
