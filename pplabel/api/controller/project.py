import sqlalchemy
from marshmallow import fields
import numpy as np

from ..model import Project
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
    print("****************** postadd ", new_project.data_dir, new_project.label_dir)
    print(
        "****************** create outpt",
        Classification(new_project).single_class_importer(),
    )
    return new_project


get_all, get, post, put, delete = crud(
    Project,
    ProjectSchema,
    triggers=[pre_add, post_add],
)
