from flask import make_response, abort, request

from pplabel.config import db
from .model import Project
from .schema import ProjectSchema


def search():  # read_all
    projects = Project.query.all()
    return ProjectSchema(many=True).dump(projects), 200


def get(project_id):  # read_one
    project = Project.query.filter(Project.project_id == project_id).one_or_none()

    if project is not None:
        schema = ProjectSchema()
        return schema.dump(project)
    abort(404, f"Project not found for Id: {project_id}")


def post():  # create
    new_project = request.get_json()
    schema = ProjectSchema()

    print("request body", type(new_project), new_project)
    print("validate", schema.validate(new_project))

    new_project = schema.load(new_project)
    print("after load", type(new_project), new_project)
    db.session.add(new_project)
    db.session.commit()
    return schema.dump(new_project), 201


# def put(project_id, project):
#     pass


def delete(project_id):
    project = Project.query.filter(Project.project_id == project_id).one_or_none()

    if project is None:
        abort(404, f"Project {project_id} don't exist int the databae.")

    db.session.delete(project)
    db.session.commit()
    return make_response(f"Project {project_id} deleted", 200)
