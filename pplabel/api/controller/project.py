import math
import random

import sqlalchemy
from marshmallow import fields
import numpy as np
import connexion

from pplabel.config import db
from ..model import Project, Label, Annotation, Task, Data, TaskCategory
from ..schema import ProjectSchema
from .base import crud
from . import label
from ..util import abort
import pplabel.task


def pre_add(new_project, se):
    new_labels = new_project.labels
    rets, unique = label.unique_within_project(new_project.project_id, new_labels)
    if not np.all(unique):
        # TODO: return the not unique field
        abort("Project labels are not unique", 409)
    return new_project


default_imexporter = {
    "classification": "single_class",
    "detection": "coco",
    "segmentation": "mask",
}  # TODO: remove this


def exportDataset(project_id):
    _, project = Project._exists(project_id)
    task_category = TaskCategory._get(task_category_id=project.task_category_id)
    handler = eval(task_category.handler)(project)
    if project.format is not None:
        exporter = handler.exporters[project.format]
    else:
        exporter = handler.exporters[default_imexporter[project.task_category.name]]
    req = connexion.request.json
    exporter(req["export_dir"])


def post_add(new_project, se):
    task_category = TaskCategory._get(task_category_id=new_project.task_category_id)
    # try:
    handler = eval(task_category.handler)(new_project)
    if new_project.format is not None:
        if new_project.format not in handler.importers.keys():
            abort(f"Importer {new_project.format} not found", 500, "No such importer")
        importer = handler.importers[new_project.format]
    else:
        importer = handler.importers[default_imexporter[new_project.task_category.name]]
    importer()

    # except Exception as e:
    #     abort(e, 500, "Import dataset failed")

    # TODO: add readme file to project dir
    return new_project


def pre_delete(project, se):
    return project


def post_delete(project, se):
    pass


def split_dataset(project_id, epsilon=1e-3):
    Project._exists(project_id)
    split = connexion.request.json
    if list(split.keys()) != ["train", "validation", "test"] or len(split) != 3:
        abort(
            f"Got {split}",
            500,
            "Request should provide train, validataion and test percentage",
        )  # TODO: change response code
    if abs(1 - sum(split.values())) > epsilon:
        abort(
            f"The train({split['train']}), validation({split['validation']}), test({split['test']}) split don't sum to 1.",
            500,
            "The three percentage don't sum to 1",
        )  # TODO: change response code
    split_num = [0] * 4
    split_num[0] = 0
    split_num[1] = split["train"]
    split_num[2] = split["validation"]
    split_num[3] = split["test"]
    split = split_num
    for idx in range(1, 4):
        split[idx] += split[idx - 1]

    tasks = Task._get(project_id=project_id, many=True)
    split = [math.ceil(s * len(tasks)) for s in split]
    print(len(tasks), split)
    random.shuffle(tasks)
    for set in range(3):
        for idx in range(split[set], split[set + 1]):
            print(idx)
            tasks[idx].set = set
    db.session.commit()
    tasks = Task._get(project_id=project_id, many=True)
    return {
        "train": split[1],
        "validation": split[2] - split[1],
        "test": split[3] - split[2],
    }, 200


get_all, get, post, put, delete = crud(
    Project,
    ProjectSchema,
    triggers=[pre_add, post_add, pre_delete],
)
