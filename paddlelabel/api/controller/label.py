import random

import numpy as np
from sqlalchemy.sql.expression import func
import connexion

from paddlelabel.config import db
from paddlelabel.api.util import abort
from .base import crud
from ..model import Label, Project, Annotation
from ..schema import LabelSchema
from ..util import abort
from paddlelabel.task.util import rand_hex_color


# TODO: simplify with _get
def unique_within_project(project_id, new_labels=[], col_names=["id", "name"]):
    """check whether label id and name is unique within project

    Parameters
    ----------
    project_id : int
        The project labels belong to
    new_labels : [[], [], ..., []]
        The labels to be checked, each contains propreties of a new label
    col_names : ["", "", ..., ""]
        Column names to be checked

    Returns
    -------
    list
        [[True/False, ...,True/False], ..., [True/False, ...,True/False]]
        Whether each label is unique
    list
        [True/False, ...,True/False]
        When there's only one input
    """
    labels = Label.query.filter(Label.project_id == project_id).all()
    rets = []
    for column_idx, column_name in enumerate(col_names):
        results = [True] * len(new_labels)
        curr_values = set()
        for label in labels:
            curr_values.add(getattr(label, column_name))
        new_values = set()
        for idx, new_label in enumerate(new_labels):
            new_value = getattr(new_label, column_name)
            if new_value in curr_values:
                results[idx] = False
                continue
            if new_value in new_values:
                results[idx] = False
                continue
            new_values.add(new_value)
        rets.append(results)
    rets = np.array(rets)
    unique = np.all(rets, axis=0)

    if len(rets) == 1:
        return rets[0], unique[0]
    return rets, unique


def pre_add(new_label, se):
    # 1. label must have project_id and project must exist,
    if new_label.project_id is None:
        abort("Must specify project_id", 400)
    Project._exists(new_label.project_id)

    # 2. generate id, color
    if new_label.id is None:
        maxid = se.query(func.max(Label.id)).filter_by(project_id=new_label.project_id).one()[0]
        if maxid is None:
            maxid = 0
        new_label.id = maxid + 1
    if new_label.color is None:
        colors = Label.query.with_entities(Label.color).filter(Label.project_id == new_label.project_id).all()
        colors = [c[0] for c in colors]
        new_label.color = rand_hex_color(colors)

    # 3. cols must be unique within project
    cols = ["id", "name", "color"]
    rets, unique = unique_within_project(new_label.project_id, [new_label], cols)
    if not unique[0]:
        not_unique_cols = ", ".join([c for c, u in zip(cols, rets) if not u])
        abort(f"Label {not_unique_cols} is not unique", 409)

    return new_label


def in_use(label_id):
    annotations = Annotation.query.filter(Annotation.label_id == label_id).all()
    if len(annotations) == 0:
        return False
    return True


def pre_delete(label, se):
    if in_use(label.label_id):
        abort(f"Can't delete label {label.name} with annotation record", 409)
    sub_catgs = Label._get(super_category_id=label.label_id, many=True)
    print("sub_catgs", sub_catgs)
    if len(sub_catgs) != 0:
        abort(f"Can't delete label {label.name} which is super category to other labels", 409)
    return label


def get_by_project(project_id):
    Project._exists(project_id)
    labels = Label.query.filter(Label.project_id == project_id).all()
    return LabelSchema(many=True).dump(labels), 200


def delete_by_project(project_id, project_exists=False):
    if not project_exists:
        Project._exists(project_id)
    labels = Label._get(project_id=project_id, many=True)
    for lab in labels:
        db.session.delete(lab)
    db.session.commit()


def set_by_project(project_id):
    # _, project = Project._exists(project_id)
    # delete_by_project(project_id, project_exists=True)
    # schema = LabelSchema(many=True)
    # labels = schema.load(connexion.request.json)
    # for lab in labels:
    #     project.labels.append(lab)
    # db.session.commit()
    # return schema.dump(project.labels), 200
    abort("Not implemented", 500, "Not implemented")


get_all, get, post, put, delete = crud(Label, LabelSchema, triggers=[pre_add, pre_delete])


# TODO: abstract to any column

"""
label_id = nncol(db.Integer(), primary_key=True)
id = nncol(db.Integer())
project_id = db.Column(
    db.Integer(), db.ForeignKey("project.project_id", ondelete="CASCADE")
)
name = nncol(db.String())
color = db.Column(db.String())
comment = db.Column(db.String())
created = nncol(db.DateTime, default=datetime.utcnow)
modified = nncol(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

- [x]. id unique within project
- [x]. name unique within project
- [x]. label with annotation in use cant be deleted

"""
