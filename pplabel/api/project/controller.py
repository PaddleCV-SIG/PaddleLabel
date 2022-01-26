import json
import functools

from flask import make_response, abort, request
import sqlalchemy

from pplabel.config import db
from pplabel.api import base
from pplabel.api.base import immutable_properties
from .model import Project
from .schema import ProjectSchema

get_all = functools.partial(base.get_all, Project, ProjectSchema)

get = functools.partial(base.get, Project, ProjectSchema)

post = functools.partial(base.post, Project, ProjectSchema)

put = functools.partial(base.put, Project, ProjectSchema)

delete = functools.partial(base.delete, Project, ProjectSchema)


# def delete(project_id):
#     project = Project.query.filter(Project.project_id == project_id).one_or_none()
#
#     if project is None:
#         abort(404, f"Project {project_id} don't exist int the databae.")
#
#     db.session.delete(project)
#     db.session.commit()
#     return make_response(f"Project {project_id} deleted", 200)
