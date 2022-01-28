from flask import make_response, abort, request

from pplabel.config import db
from pplabel.api.base.controller import crud
from .model import Annotation
from .schema import AnnotationSchema


get_all, get, post, put, delete = crud(Annotation, AnnotationSchema)
