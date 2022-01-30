from flask import make_response, abort

from .base import crud
from ..model import Annotation, Task
from ..schema import AnnotationSchema
from ..util import abort

# from .. import project


# TODO: do we really need project id?
def pre_add(annotation, se):
    print("annotation pre add asdfadsfasdf")
    task = Task.query.filter(Task.task_id == annotation.task_id).one_or_none()
    if task is None:
        abort(f"No task with task id {annotation.task_id}", 404)
    annotation.project_id = task.project_id
    return annotation


get_all, get, post, put, delete = crud(Annotation, AnnotationSchema, [pre_add])


# def get_by_project(project_id, instance=False):
#     annotations = Annotation.query.filter(Annotation.project_id == project_id).all()
#     if instance:
#         return annotations
#     if len(annotations) == 0:
#         if project.controller.get_by_id(project_id) is None:
#             abort(404, f"No project with project id: {project_id}")
#
#     return AnnotationSchema(many=True).dump(annotations), 200
#
#
# def get_by_label(label_id, instance=False):
#     annotations = Annotation.query.filter(Annotation.label_id == label_id).all()
#     if instance:
#         return annotations
#     if len(annotations) == 0:
#         if label.controller.get_by_id(label_id) is None:
#             msg = f"No label with label id : {label_id}"
#             return msg, 404, {"message": msg}
#     return AnnotationSchema(many=True).dump(annotations), 200
