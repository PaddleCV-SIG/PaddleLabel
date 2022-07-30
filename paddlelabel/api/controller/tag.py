import connexion

from paddlelabel.config import db
from .base import crud
from ..model import Tag, Project, Task, TagTask
from ..schema import TagSchema, TagTaskSchema
from ..util import abort


def pre_add(new_tag, se):
    curr_tag = Tag._get(project_id=new_tag.project_id, name=new_tag.name)
    if curr_tag is not None:
        abort(
            f"Duplicate tag with tag name {new_tag.name} under project {new_tag.project_id}",
            409,
        )
    return new_tag


get_all, get, post, put, delete = crud(Tag, TagSchema, [pre_add])


def get_by_project(project_id):
    Project._exists(project_id)
    tags = Tag._get(project_id=project_id, many=True)
    return TagSchema(many=True).dump(tags), 200


def get_by_task(task_id):
    Task._exists(task_id)
    tag_tasks = TagTask._get(task_id=task_id, many=True)
    tags = []
    for tag_task in tag_tasks:
        tag = Tag._get(tag_id=tag_task.tag_id)
        tags.append(tag)
    return TagSchema(many=True).dump(tags), 200


def add_to_task(task_id):
    # 1. check
    # 1.1 check task exists
    task = Task._get(task_id=task_id)
    if task is None:
        abort(f"No task with task id {task_id}", 404)

    body = connexion.request.json
    tag_id = body["tag_id"]
    # 1.2 check tag exist
    tag = Tag._get(tag_id=tag_id)
    if tag is None:
        abort(f"No tag with tag id {tag_id}", 404)
    # 1.3 no duplicate records
    curr_tag_task = TagTask._get(task_id=task_id, tag_id=tag_id)
    if curr_tag_task is not None:
        abort(f"Task {task_id} is already tagged {tag_id}", 409)
    # 1.4 check tag under task
    project_id = Task._get(task_id=task_id).project_id
    if tag.project_id != project_id:
        abort(f"Tag {tag_id} is not under project {project_id}", 404)

    tag_task = TagTask(
        tag_id=tag_id,
        task_id=task_id,
        project_id=task.project_id,
    )
    db.session.add(tag_task)
    db.session.commit()
    tag_tasks = TagTask._get(task_id=task_id, many=True)
    tags = []
    for tag_task in tag_tasks:
        tags.append(tag_task.tag)
    return TagSchema(many=True).dump(tags), 201
