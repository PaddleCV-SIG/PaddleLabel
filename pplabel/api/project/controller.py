import json
import functools
import os.path as osp
import os

from flask import make_response, abort, request
import sqlalchemy
from marshmallow import fields

import pplabel
from ..base.controller import crud
from ..base.model import immutable_properties
from .model import Project
from .schema import ProjectSchema


def pre_add(project, se):
    # task_category = project.get_task_category()
    # project.label_config = eval(task_category.handler)().dumps(project.label_config)
    project.label_config = pplabel.core.classification.LabelConfig().dumps(
        project.label_config
    )

    return project


get_all, get, post, put, delete = crud(Project, ProjectSchema, triggers=[pre_add])
