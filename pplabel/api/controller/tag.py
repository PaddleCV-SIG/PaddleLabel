from .base import crud
from ..model import Tag, Task, Project
from ..schema import TagSchema
from ..util import abort


def pre_add(new_tag, se):
    tags = Tag._get(project_id=new_tag.project_id, many=True)
    for tag in tags:
        if tag.name == new_tag.name:
            abort(409, f"Tag name {tag.name} is not unique under the project")
    return new_tag


get_all, get, post, put, delete = crud(Tag, TagSchema, [pre_add])


def get_by_project(project_id):
    Project._exists(project_id)
    tags = Tag._get(project_id=project_id, many=True)
    return TagSchema(many=True).dump(tags), 200
