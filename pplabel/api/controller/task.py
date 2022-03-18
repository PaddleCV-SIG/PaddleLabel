import json
import random
import math

import numpy as np

import connexion
from pplabel.config import db
from .base import crud
from ..model import Task, Project
from ..schema import TaskSchema
from . import project
from pplabel.api.util import abort

# TODO: reject tasks with same datas
get_all, get, post, put, delete = crud(Task, TaskSchema)


def get_by_project(project_id):
    if connexion.request.method == "HEAD":
        return get_stat_by_project(project_id)
    Project._exists(project_id)
    tasks = Task.query.filter(Task.project_id == project_id).all()
    return TaskSchema(many=True).dump(tasks), 200


# TODO: dont lazy load annotations in tasks
def get_stat_by_project(project_id):
    Project._exists(project_id)
    tasks = Task.query.filter(Task.project_id == project_id).all()
    ann_count = 0
    for task in tasks:
        if len(task.annotations) != 0:
            ann_count += 1
    res = {"finished": ann_count, "total": len(tasks)}
    return res, 200, res


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
