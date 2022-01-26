import json
import functools
import os.path as osp
import os

from flask import make_response, abort, request
import sqlalchemy

from pplabel.config import db
from pplabel.api import base
from pplabel.api.base import immutable_properties
from .model import Project
from .schema import ProjectSchema


def pre_add(new_item, se):
    # TODO: check the file path is valid
    # TODO: https://gist.github.com/mo-han/240b3ef008d96215e352203b88be40db
    if not osp.isdir(new_item.data_dir):
        try:
            os.makedirs(new_item.data_dir)
        except Exception as e:
            abort(500, f"Create data dir {new_item.data_dir} failed. Exception: {e}")
    if new_item.label_dir is not None and not osp.isdir(new_item.label_dir):
        try:
            os.makedirs(new_item.label_dir)
        except:
            abort(500, f"Create label dir {new_item.label_dir} failed. Exception: {e}")


get_all, get, post, put, delete = base.crud(Project, ProjectSchema, triggers=[pre_add])
