from .base import crud
from ..model import Annotation, Task, Project, Data
from ..schema import AnnotationSchema
from ..util import abort


def pre_add(annotation, se):
    data = Data._get(data_id=annotation.data_id)
    if data is None:
        abort(f"No data with data_id {data_id}")
    task = Task._get(task_id=data.task_id)
    if task is None:
        abort(f"No task with task id {annotation.task_id}", 404)

    annotation.task_id = data.task_id
    annotation.project_id = task.project_id
    # if annotation.type is None:
    #     annotation.type = "json"

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
