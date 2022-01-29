from flask import make_response, abort, request

from pplabel.config import db

from ..base.controller import crud
from ..base.model import immutable_properties
from .model import Label
from .schema import LabelSchema


get_all, get, post, put, delete = crud(Label, LabelSchema)
