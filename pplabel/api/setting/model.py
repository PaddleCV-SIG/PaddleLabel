from functools import total_ordering

from pplabel.serve import db
from pplabel.api.util import nncol


# Todo: add unique
class TaskCategory(db.Model):
    __tablename__ = "taskCategory"
    task_category_id = nncol(db.Integer(), primary_key=True, autoincrement=False)
    # db.Integer(), primary_key=True)
    name = nncol(db.String())
    handler = db.Column(db.String())

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
