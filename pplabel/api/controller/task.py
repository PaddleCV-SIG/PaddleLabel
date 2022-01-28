from flask import make_response, abort, request

from pplabel.api import base
from pplabel.config import db

# from .model import Task
from pplabel.api.model import Task
from ..schema import TaskSchema


def post_get_all(items, se):
    # print("+_+_+_+", items[0].project.name)
    pass


def post_post(new_item, se):
    print("_________________", new_item.project)


get_all, get, post, put, delete = base.crud(
    Task, TaskSchema, triggers=[post_get_all, post_post]
)
