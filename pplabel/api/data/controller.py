from flask import make_response, abort, request

from pplabel.serve import db

from ..base.controller import crud
from ..base.model import immutable_properties
from .model import Data
from .schema import DataSchema


get_all, get, post, put, delete = crud(Data, DataSchema)
