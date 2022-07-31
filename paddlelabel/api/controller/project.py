import math
import random
import json
import requests
import os
import os.path as osp
import base64
from copy import deepcopy
import traceback

import numpy as np
import connexion

from paddlelabel.config import db
from paddlelabel.api.model import Project, Task, TaskCategory, Annotation, Label, project
from paddlelabel.api.schema import ProjectSchema
from paddlelabel.api.controller.base import crud
from paddlelabel.api.controller import label
from paddlelabel.api.util import abort
from paddlelabel.task.util import rand_hex_color
from paddlelabel.util import camel2snake
from paddlelabel.task.util.file import (
    image_extensions,
    listdir,
    create_dir,
    remove_dir,
    copy,
)
import paddlelabel


def pre_add(new_project, se):
    if not osp.isabs(new_project.data_dir):
        abort("Dataset Path is not absolute path", 409)

    new_project.label_format = camel2snake(new_project.label_format)
    new_labels = new_project.labels
    rets, unique = label.unique_within_project(new_project.project_id, new_labels)
    if not np.all(unique):
        # TODO: return the not unique field
        abort("Project labels are not unique", 409)
    return new_project


def _import_dataset(project, data_dir=None):
    task_category = TaskCategory._get(task_category_id=project.task_category_id)

    # 1. create handler
    if task_category is None:
        handler = paddlelabel.task.BaseTask(project)
    else:
        handler = eval(task_category.handler)(project, data_dir=data_dir)

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
    try:
        _import_dataset(new_project)
    except Exception as e:
        project = Project.query.filter(Project.project_id == new_project.project_id).one()
        db.session.delete(project)
        db.session.commit()

        print("Create project failed")
        print(traceback.format_exc())

        if "detail" in dir(e):
            abort(e.detail, 500, e.title)
        else:
            abort(str(e), 500, str(e))

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

    try:
        exporter(req["export_dir"])
    except Exception as e:
        abort(str(e), 500, str(e))


def import_dataset(project_id):
    """import additional data

    Args:
        project_id (int): the project to import to
    """
    # 1. get project
    req = connexion.request.json
    _, project = Project._exists(project_id)

    # 2. get current project data names
    tasks = Task._get(project_id=project.project_id, many=True)
    curr_data_names = set()
    for task in tasks:
        for data in task.datas:
            curr_data_names.add(osp.basename(data.path))

    # 3. move all new images and all other files to import temp
    import_temp = osp.join(project.data_dir, "import_temp")
    create_dir(import_temp)

    import_dir = req["import_dir"]
    new_data_paths = listdir(
        import_dir,
        filters={"exclude_prefix": ["."], "include_postfix": image_extensions},
    )
    all_paths = listdir(
        import_dir,
        filters={"exclude_prefix": ["."]},
    )
    all_copy_paths = [p for p in all_paths if p not in new_data_paths]
    new_data_paths = [p for p in new_data_paths if osp.basename(p) not in curr_data_names]
    all_copy_paths += new_data_paths
    # print(all_copy_paths)
    for p in all_copy_paths:
        copy(osp.join(import_dir, p), osp.join(import_temp, p))

    _import_dataset(project, import_temp)

    for p in new_data_paths:
        copy(osp.join(import_temp, p), osp.join(project.data_dir, p))

    remove_dir(import_temp)


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
    # print("split numbers: ", len(tasks), split)
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
    color = rand_hex_color([l.color for l in project.labels])
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
    # print("request url", url)

    headers = {"content-type": "application/json"}

    labels = Label._get(project_id=project_id, many=True)
    labels = {l.name: l.label_id for l in labels}

    for task in Task._get(project_id=project_id, many=True):
        for data in task.datas:
            if len(data.annotations) != 0:
                continue
            if params["same_server"]:
                body = {"img": osp.join(project.data_dir, data.path), "format": "path"}
            else:
                img_b64 = base64.b64encode(open(osp.join(project.data_dir, data.path), "rb").read()).decode("utf-8")
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
            # print(osp.join(project.data_dir, data.path), res["result"])
    db.session.commit()
    return "finished"


def post_delete(project, se):
    warning_path = osp.join(project.data_dir, "paddlelabel.warning")
    if osp.exists(warning_path):
        os.remove(warning_path)


get_all, get, post, put, delete = crud(
    Project,
    ProjectSchema,
    triggers=[pre_add, post_add, pre_put, post_delete],
)
