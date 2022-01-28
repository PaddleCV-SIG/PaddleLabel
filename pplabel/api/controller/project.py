import json
import functools
import os.path as osp
import os

from flask import make_response, abort, request
import sqlalchemy

from pplabel.config import db
from .base import crud
from ..model.base import immutable_properties
from ..model import Project
from ..schema import ProjectSchema


def create_dir(**kwargs):
    for name, path in kwargs.items():
        print("++++", name, path)
        if path is None:
            return
        if not osp.isabs(path):
            abort(500, f"Only support absolute path, {name}: {path} is not")
        if not osp.isdir(path):
            try:
                os.makedirs(path)
                print("created: ", path)
            except Exception as e:
                abort(500, f"Create {name} {path} failed. Exception: {e}")


def post_add(project, se):
    # TODO: check the file path is valid
    # TODO: https://gist.github.com/mo-han/240b3ef008d96215e352203b88be40db
    create_dir(data_dir=project.data_dir, label_dir=project.label_dir)


def post_put(project, se):
    create_dir(data_dir=project.data_dir, label_dir=project.label_dir)


get_all, get, post, put, delete = crud(
    Project, ProjectSchema, triggers=[post_add, post_put]
)
