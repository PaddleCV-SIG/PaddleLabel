from flask import make_response, abort

from pplabel.api.base.controller import crud
from .model import Annotation
from .schema import AnnotationSchema

from .. import project

get_all, get, post, put, delete = crud(Annotation, AnnotationSchema)


def get_by_project(project_id, instance=False):
    annotations = Annotation.query.filter(Annotation.project_id == project_id).all()
    if instance:
        return annotations
    if len(annotations) == 0:
        if project.controller.get_by_id(project_id) is None:
            abort(404, f"No project with project id: {project_id}")

    return AnnotationSchema(many=True).dump(annotations), 200
