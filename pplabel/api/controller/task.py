from flask import make_response, abort, request

from pplabel.config import db
from .base import crud
from ..model.base import immutable_properties
from ..model import Task
from ..schema import TaskSchema

# TODO: reject tasks with same datas
get_all, get, post, put, delete = crud(Task, TaskSchema)
