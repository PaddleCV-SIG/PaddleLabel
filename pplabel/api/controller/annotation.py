from .base import crud
from ..model import Annotation, Task, Project
from ..schema import AnnotationSchema
from ..util import abort

# TODO: do we really need project id?
def pre_add(annotation, se):
    print("annotation pre add asdfadsfasdf")
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
