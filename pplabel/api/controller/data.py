from flask import make_response, abort, request

from pplabel.config import db
from .base import crud
from ..model.base import immutable_properties
from ..model import Data
from ..schema import DataSchema


def post_get_all(items, se):
    # print("+_+_+_+", items[0].project.name)
    pass


def post_post(new_item, se):
    print("_________________", new_item.project)


get_all, get, post, put, delete = crud(
    Data, DataSchema, triggers=[post_get_all, post_post]
)
