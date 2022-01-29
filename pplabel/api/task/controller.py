from flask import make_response, abort, request

from pplabel.config import db
from ..base.controller import crud
from ..base.model import immutable_properties
from .model import Task
from .schema import TaskSchema
import pplabel


# TODO: reject tasks with same datas
get_all, get, post, put, delete = crud(Task, TaskSchema)


# def post():
#     # pplabel.core.classification.classification_single.import_project(
#     pplabel.core.classification.import_project(
#         1,
#         "/home/lin/Desktop/data/pplabel/single_clas_toy/PetImages/",
#         filters={"exclude_prefix": ["."], "exclude_postfix": [".db"]},
#     )
