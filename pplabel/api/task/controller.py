from flask import make_response, abort, request

from pplabel.config import db
from ..base.controller import crud
from ..base.model import immutable_properties
from .model import Task
from .schema import TaskSchema

# TODO: reject tasks with same datas
get_all, get, post, put, delete = crud(Task, TaskSchema)
