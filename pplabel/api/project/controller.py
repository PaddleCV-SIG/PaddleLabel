import json
import functools
import os.path as osp
import os

from flask import make_response, abort, request
import sqlalchemy
from marshmallow import fields
import numpy as np

import pplabel
from ..base.controller import crud
from ..base.model import immutable_properties
from .model import Project
from .schema import ProjectSchema
from ..label.controller import unique_within_project


def pre_add(new_project, se):
    new_labels = new_project.labels
    rets, unique = unique_within_project(new_project.project_id, new_labels)
    if not np.all(unique):
        # TODO: return not unique field
        # TODO: change ret code
        abort(500, "Project labels are not unique")
    return new_project


get_all, get, post, put, delete = crud(
    Project,
    ProjectSchema,
    immutables=immutable_properties + ["project_id"],
    triggers=[pre_add],
)
