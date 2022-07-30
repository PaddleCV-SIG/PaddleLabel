import connexion
from paddlelabel.config import db
from .base import crud
from ..model import Task, Project
from ..schema import TaskSchema
from paddlelabel.api.util import abort, parse_order_by

# TODO: reject tasks with same datas
get_all, get, post, put, delete = crud(Task, TaskSchema)


def get_by_project(project_id, order_by="created asc"):
    if connexion.request.method == "HEAD":
        return get_stat_by_project(project_id)
    Project._exists(project_id)
    order = parse_order_by(Task, order_by)

    tasks = Task.query.filter(Task.project_id == project_id).order_by(order).all()
    return TaskSchema(many=True).dump(tasks), 200


# TODO: dont lazy load annotations in tasks
def get_stat_by_project(project_id):
    Project._exists(project_id)
    tasks = Task.query.filter(Task.project_id == project_id).all()
    ann_count = 0
    for task in tasks:
        if len(task.annotations) != 0:
            ann_count += 1
    res = {"finished": ann_count, "total": len(tasks)}
    return res, 200, res
