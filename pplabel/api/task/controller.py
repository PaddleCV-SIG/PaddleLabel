from flask import make_response, abort, request

from pplabel.api import base
from pplabel.config import db
from .model import Task
from .schema import TaskSchema

get_all, get, post, put, delete = base.crud(Task, TaskSchema)
