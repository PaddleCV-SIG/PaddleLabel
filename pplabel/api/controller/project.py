import json
import functools
import os.path as osp
import os

from flask import make_response, abort, request
import sqlalchemy
from marshmallow import fields
import numpy as np

import pplabel
from .base import crud
from ..model import Project
from ..schema import ProjectSchema
from .label import unique_within_project


def pre_add(new_project, se):
    new_labels = new_project.labels
    rets, unique = unique_within_project(new_project.project_id, new_labels)
    if not np.all(unique):
        # TODO: return not unique field
        abort(409, "Project labels are not unique")
    return new_project


get_all, get, post, put, delete = crud(
    Project,
    ProjectSchema,
    triggers=[pre_add],
)


def get_by_id(project_id):
    project = Project.query.filter(Project.project_id == project_id).one_or_none()
    return project
