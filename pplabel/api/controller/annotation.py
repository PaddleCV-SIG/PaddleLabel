from .base import crud
from ..model import Annotation, Task, Project, Data
from ..schema import AnnotationSchema
from ..util import abort


def pre_add(annotation, se):
    task = Task.query.filter(Task.task_id == annotation.task_id).one_or_none()
    if task is None:
        abort(f"No task with task id {annotation.task_id}", 404)
    annotation.project_id = task.project_id
    return annotation


get_all, get, post, put, delete = crud(Annotation, AnnotationSchema, [pre_add])


def get_by_project(project_id):
    Project._exists(project_id)
    anns = Annotation._get(project_id=project_id, many=True)
    return AnnotationSchema(many=True).dump(anns), 200


def get_by_task(task_id):
    Task._exists(task_id)
    anns = Annotation._get(task_id=task_id, many=True)
    return AnnotationSchema(many=True).dump(anns), 200


def get_by_data(data_id):
    Data._exists(data_id)
    anns = Annotation._get(data_id=data_id, many=True)
    return AnnotationSchema(many=True).dump(anns), 200
