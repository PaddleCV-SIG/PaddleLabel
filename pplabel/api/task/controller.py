from flask import make_response, abort, request

from pplabel.config import db
from .model import Task
from .schema import TaskSchema


def get_all():
    tasks = Task.query.all()
    return TaskSchema(many=True).dump(tasks), 200


def get(task_id):
    task = Task.query.filter(Task.task_id == task_id).one_or_none()

    if task is not None:
        return TaskSchema().dump(task)
    abort(404, f"Task not found for Id: {task_id}")


def post():
    new_task = request.get_json()
    schema = TaskSchema()
    new_task = schema.load(new_task)

    print("new_task", new_task)
    db.session.add(new_task)
    db.session.commit()
    return schema.dump(new_task), 201


def put(project_id, project):
    pass


def delete(project_id):
    pass
