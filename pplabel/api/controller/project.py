import sqlalchemy
from marshmallow import fields
import numpy as np

from ..model import Project, Label, Annotation, Task, Data, TaskCategory
from ..schema import ProjectSchema
from .base import crud
from . import label
from ..util import abort
import pplabel.task


def pre_add(new_project, se):
    new_labels = new_project.labels
    rets, unique = label.unique_within_project(new_project.project_id, new_labels)
    if not np.all(unique):
        # TODO: return the not unique field
        abort("Project labels are not unique", 409)
    return new_project


default_importer = {"classification": "single_class", "detection": "coco"}  # TODO: remove this


def post_add(new_project, se):
    task_category = TaskCategory._get(task_category_id=new_project.task_category_id)
    # try:
    handler = eval(task_category.handler)(new_project)
    if new_project.format is not None:
        importer = handler.importers[new_project.format]
    else:
        importer = handler.importers[default_importer[new_project.task_category.name]]
    importer()

    # except Exception as e:
    #     abort(e, 500, "Import dataset failed")

    return new_project


def pre_delete(project, se):
    return project


def post_delete(project, se):
    pass


get_all, get, post, put, delete = crud(
    Project,
    ProjectSchema,
    triggers=[pre_add, post_add, pre_delete],
)
