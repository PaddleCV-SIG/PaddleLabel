import json

from flask import make_response, abort, request
import connexion

from pplabel.config import db
from .base import crud
from ..model import Task
from ..schema import TaskSchema

# from .. import project
# from .. import annotation

# TODO: reject tasks with same datas
get_all, get, post, put, delete = crud(Task, TaskSchema)


# def get_by_project(project_id, instance=False):
#     if connexion.request.method == "HEAD":
#         return get_stat_by_project(project_id, instance=instance)
#     tasks = Task.query.filter(Task.project_id == project_id).all()
#     if instance:
#         return tasks
#     if len(tasks) == 0:
#         if project.controller.get_by_id(project_id) is None:
#             abort(404, f"No project with project id: {project_id}")
#     return TaskSchema(many=True).dump(tasks), 200
#
#
# # TODO: dont lazy load annotations in tasks
# def get_stat_by_project(project_id, instance=False):
#     tasks = Task.query.filter(Task.project_id == project_id).all()
#     if not instance and len(tasks) == 0:
#         if project.controller.get_by_id(project_id) is None:
#             return "", 404, {"message": f"No project with project id {project_id}"}
#     ann_count = 0
#     for task in tasks:
#         if len(task.annotations) != 0:
#             ann_count += 1
#     if instance:
#         return ann_count, len(tasks)
#     res = {"finished": ann_count, "total": len(tasks)}
#     return json.dumps(res), 200, res
