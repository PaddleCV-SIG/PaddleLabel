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


def post_add(new_project, se):
    task_category = TaskCategory._get(task_category_id=new_project.task_category_id)
    eval(task_category.handler)(new_project).importers[0]()
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
