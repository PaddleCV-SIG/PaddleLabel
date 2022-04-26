import math
import random
import json
import requests
import os.path as osp
import base64

import cv2
import numpy as np
import connexion

from pplabel.config import db
from pplabel.api.model import Project, Task, TaskCategory, Annotation, Label
from pplabel.api.schema import ProjectSchema
from pplabel.api.controller.base import crud
from pplabel.api.controller import label
from pplabel.api.util import abort, rand_color
from pplabel.util import camel2snake
import pplabel


def pre_add(new_project, se):
    new_project.label_format = camel2snake(new_project.label_format)
    new_labels = new_project.labels
    rets, unique = label.unique_within_project(new_project.project_id, new_labels)
    if not np.all(unique):
        # TODO: return the not unique field
        abort("Project labels are not unique", 409)
    return new_project


default_imexporter = {"classification": "single_class", "detection": "voc"}  # TODO: remove this


def _import_dataset(project, data_dir=None):
    task_category = TaskCategory._get(task_category_id=project.task_category_id)

    # 1. create handler
    if task_category is None:
        handler = pplabel.task.BaseTask(project)
    else:
        handler = eval(task_category.handler)(project)

    # 2. choose importer. if specified, use importer for new_project.label_format, else use default_importer
    if project.label_format is not None:
        if project.label_format not in handler.importers.keys():
            abort(
                f"Importer {project.label_format} for project category {task_category.name} not found",
                404,
                "No such importer",
            )
        importer = handler.importers[project.label_format]
    else:
        importer = handler.default_importer

    # 3. run import
    importer(data_dir)


def post_add(new_project, se):
    """run task import after project creation"""
    _import_dataset(new_project)

    # TODO: add readme file to project dir
    return new_project


def export_dataset(project_id):
    _, project = Project._exists(project_id)
    task_category = TaskCategory._get(task_category_id=project.task_category_id)
    handler = eval(task_category.handler)(project)
    if project.label_format is not None:
        exporter = handler.exporters[project.label_format]
    else:
        exporter = handler.default_exporter
    req = connexion.request.json
    exporter(req["export_dir"])


def import_dataset(project_id):
    req = connexion.request.json
    _, project = Project._exists(project_id)
    _import_dataset(project, req["import_dir"])


def pre_put(project, body, se):
    if "other_settings" in body.keys():
        body["other_settings"] = json.dumps(body["other_settings"])
    return project, body


def split_dataset(project_id, epsilon=1e-3):
    Project._exists(project_id)
    split = connexion.request.json
    if list(split.keys()) != ["train", "val", "test"]:
        abort(
            f"Got {split}",
            500,
            "Request should provide train, validataion and test percentage",
        )  # TODO: change response code
    if abs(1 - sum(split.values())) > epsilon:
        abort(
            f"The train({split['train']}), val({split['val']}), test({split['test']}) split don't sum to 1.",
            500,
            "The three percentages don't sum to 1",
        )  # TODO: change response code
    split_num = [0] * 4
    split_num[1] = split["train"]
    split_num[2] = split["val"]
    split_num[3] = split["test"]
    split = split_num
    for idx in range(1, 4):
        split[idx] += split[idx - 1]

    tasks = Task._get(project_id=project_id, many=True)
    split = [math.ceil(s * len(tasks)) for s in split]
    print("split numbers: ", len(tasks), split)
    random.shuffle(tasks)
    for set in range(3):
        for idx in range(split[set], split[set + 1]):
            tasks[idx].set = set
    db.session.commit()
    tasks = Task._get(project_id=project_id, many=True)
    return {
        "train": split[1],
        "val": split[2] - split[1],
        "test": split[3] - split[2],
    }, 200


def create_label(project, label_name):
    color = rand_color([l.color for l in project.labels])
    ids = [l.id for l in project.labels]
    ids.append(0)
    label = Label(
        id=max(ids) + 1,
        project_id=project.project_id,
        name=label_name,
        color=color,
    )
    project.labels.append(label)
    db.session.commit()
    return label


def predict(project_id):
    _, project = Project._exists(project_id)

    params = connexion.request.json
    if "create_label" not in params.keys():
        params["create_label"] = False
    if "same_server" not in params.keys():
        params["same_server"] = False

    url = params["ml_backend_url"]
    if url[-1] != "/":
        url += "/"
    url += params["model"] + "/predict"
    print("request url", url)

    headers = {"content-type": "application/json"}

    labels = Label._get(project_id=project_id, many=True)
    labels = {l.name: l.label_id for l in labels}
    

    for task in Task._get(project_id=project_id, many=True):
        for data in task.datas:
            if params["same_server"]:
                body = {"img": osp.join(project.data_dir, data.path), "format": "path"}
            else:
                img_b64 = base64.b64encode(
                    open(osp.join(project.data_dir, data.path), "rb").read()
                ).decode("utf-8")
                body = {"img": img_b64, "format": "b64"}
            res = requests.post(url, headers=headers, json=body)
            res = json.loads(res.text)
            if res["result"] not in labels.keys():
                if params["create_label"]:
                    new_label = create_label(project, res["result"])
                    labels[new_label.name] = new_label.id
                else:
                    continue
            ann = Annotation(
                label_id=labels[res["result"]],
                project_id=project.project_id,
                # task_id=task.task_id,
                data_id=data.data_id,
                result="",
            )
            task.annotations.append(ann)
            print(osp.join(project.data_dir, data.path), res["result"])
    db.session.commit()
    return "finished"


get_all, get, post, put, delete = crud(
    Project,
    ProjectSchema,
    triggers=[pre_add, post_add, pre_put],
)
