from flask import make_response, abort, request

from pplabel.config import db
import numpy as np

from ..base.controller import crud
from .model import Label
from .schema import LabelSchema


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
        print("curr_values", curr_values)
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
    cols = ["id", "name"]
    rets, unique = unique_within_project(new_label.project_id, [new_label], cols)
    if not unique[0]:
        not_unique_cols = ", ".join([c for c, u in zip(cols, rets) if not u])
        abort(409, f"Label {not_unique_cols} is not unique")
    return new_label


get_all, get, post, put, delete = crud(Label, LabelSchema, triggers=[pre_add])


def get_by_project(project_id):
    labels = Label.query.filter(Label.project_id == project_id).all()
    print(labels)
    return LabelSchema(many=True).dump(labels), 200


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
- [ ]. label with annotation in use cant be deleted

"""
