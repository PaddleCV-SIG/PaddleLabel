from flask import make_response, abort, request

from pplabel.config import db

from .base import crud
from ..model import Data
from ..schema import DataSchema


get_all, get, post, put, delete = crud(Data, DataSchema)
