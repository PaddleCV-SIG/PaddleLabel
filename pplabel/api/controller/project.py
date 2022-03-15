import sqlalchemy
from marshmallow import fields
import numpy as np

from ..model import Project, Label, Annotation, Task, Data
from ..schema import ProjectSchema
from .base import crud
from . import label
from ..util import abort
from ...task.classification import Classification


def pre_add(new_project, se):
    new_labels = new_project.labels
    rets, unique = label.unique_within_project(new_project.project_id, new_labels)
    if not np.all(unique):
        # TODO: return the not unique field
        abort("Project labels are not unique", 409)
    return new_project


def post_add(new_project, se):
    Classification(new_project).single_class_importer(),

    return new_project


def pre_delete(project, se):
    print("++++++project+++++", project.project_id, project)
    # Task.query.filter(Task.project_id == project.project_id).delete()
    return project


def post_delete(project, se):
    print("++++++project+++++", project.project_id, project)

    # Label.query.filter(Label.project_id == project.project_id).delete()


get_all, get, post, put, delete = crud(
    Project,
    ProjectSchema,
    triggers=[pre_add, post_add, pre_delete],
)
