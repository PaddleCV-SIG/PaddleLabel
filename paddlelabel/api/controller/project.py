# -*- coding: utf-8 -*-
import math
import random
import json
import requests
import os
import os.path as osp
import base64
from pathlib import Path

import logging
import base64

import connexion

from paddlelabel.config import db
from paddlelabel.api.model import Project, Task, TaskCategory, Annotation, Label, TaskCategory
from paddlelabel.api.schema import ProjectSchema
from paddlelabel.api.controller.base import crud
from paddlelabel.api.util import abort
from paddlelabel.task.util import rand_hex_color
from paddlelabel.util import camel2snake
from paddlelabel.task.util.file import (
    image_extensions,
    listdir,
    create_dir,
    remove_dir,
    copy,
    expand_home,
)
import paddlelabel

logger = logging.getLogger("paddlelabel")


def import_dataset(project, data_dir=None, label_format=None):
    data_dir = project.data_dir if data_dir is None else data_dir
    logger.info(f"importing dataset from {data_dir}")
    task_category = TaskCategory._get(task_category_id=project.task_category_id)

    # 1. create handler
    if task_category is None:
        handler = paddlelabel.task.BaseTask(project)
    else:
        handler = eval(task_category.handler)(project, data_dir=data_dir)

    # 2. choose importer. if specified, use importer for new_project.label_format, else use default_importer
    if label_format is None:
        label_format = None if project.label_format is None else project.label_format

    if label_format not in [None, "default"] and label_format not in handler.importers.keys():
        abort(
            f"Importer {project.label_format} for project category {task_category.name} not found",
            404,
            "No such importer",
        )
    if label_format in [None, "default"]:
        importer = handler.default_importer
    else:
        importer = handler.importers[project.label_format]

    # 3. run import
    importer(data_dir)


def import_additional_data(project_id):
    """import additional data

    Args:
        project_id (int): the project to import to
    """
    # 1. get project
    req = connexion.request.json
    _, project = Project._exists(project_id)

    # 2. get current project data file names
    tasks = Task._get(project_id=project.project_id, many=True)
    curr_data_names = set()
    for task in tasks:
        for data in task.datas:
            curr_data_names.add(Path(data.path).name)

    # 3. move all new images and all other files to import temp
    import_temp = osp.join(osp.expanduser("~"), ".paddlelabel", "import_temp")
    remove_dir(import_temp)
    create_dir(import_temp)

    import_dir = req["import_dir"]
    import_dir = expand_home(import_dir)
    import_format = req.get("import_format", None)

    if not Path(import_dir).is_absolute():
        abort(f"Only supports absolute import dir", 500)

    if not Path(import_dir).exists():
        abort(f"Import directory '{import_dir}' doesn't exist", 404)

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
    for p in all_copy_paths:
        copy(osp.join(import_dir, p), osp.join(import_temp, p), make_dir=True)

    # TODO: may have annotation for
    import_dataset(project, import_temp, "default" if import_format is None else import_format)

    for p in new_data_paths:
        copy(osp.join(import_temp, p), osp.join(project.data_dir, p), make_dir=True)

    remove_dir(import_temp)


def pre_add(new_project, se):
    new_project.data_dir = expand_home(new_project.data_dir)
    if not osp.isabs(new_project.data_dir):
        abort("Dataset Path is not absolute path", 409)
    if not Path(new_project.data_dir).exists():
        abort(f"Dataset Path {new_project.data_dir} doesn't exist", 404)

    new_project.label_format = camel2snake(new_project.label_format)
    # new_labels = new_project.labels
    # rets, unique = label.unique_within_project(new_project.project_id, new_labels)
    # print(unique)
    # if not np.all(unique):
    #     # TODO: return the not unique field
    #     abort("Project labels are not unique", 409)
    return new_project


def post_add(new_project, se):
    """run task import after project creation"""

    try:
        import_dataset(new_project)
    except Exception as e:
        project = Project.query.filter(Project.project_id == new_project.project_id).one()
        db.session.delete(project)
        db.session.commit()

        logger.exception("Create project failed", exc_info=True)

        if "detail" in dir(e):
            abort(e.detail, 500, e.title)
        else:
            abort(str(e), 500, str(e))

    return new_project


def export_dataset(project_id):
    # 1. ensure project exists
    _, project = Project._exists(project_id)

    # 2. get handler and exporter
    task_category = TaskCategory._get(task_category_id=project.task_category_id)
    handler = eval(task_category.handler)(project, is_export=True)
    export_format = connexion.request.json.get("export_format", None)
    if export_format is None:
        export_format = project.label_format
    if export_format is None or len(export_format) == 0:
        exporter = handler.default_exporter
    else:
        exporter = handler.exporters[export_format]

    # 3. get export path
    params = connexion.request.json
    params["export_dir"] = expand_home(params["export_dir"])
    if not Path(params["export_dir"]).is_absolute():
        abort(f"Only support absolute paths, got {params['export_dir']}", 500)
    if osp.exists(osp.join(params["export_dir"], "paddlelabel.warning")):
        abort(
            "This folder is actively used as file store for PaddleLabel. Please specify another folder for export", 500
        )
    # 4. export
    try:
        del params["export_format"]
        exporter(**params)

    except Exception as e:
        logging.exception("Export dataset failed")

        if "detail" in dir(e):
            abort(e.detail, 500, e.title)
        else:
            abort(str(e), 500, str(e))


def pre_put(project, body, se):
    if "other_settings" in body.keys():
        body["other_settings"] = json.dumps(body["other_settings"])
    return project, body


# TODO: move to label controller
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


def post_delete(project, se):
    warning_path = Path(project.data_dir) / "paddlelabel.warning"
    if warning_path.exists():
        warning_path.unlink()


get_all, get, post, put, delete = crud(
    Project,
    ProjectSchema,
    triggers=[pre_add, post_add, pre_put, post_delete],
)


def to_easydata(project_id):
    _, project = Project._exists(project_id)
    task_category = TaskCategory._get(task_category_id=project.task_category_id)
    handler = eval(task_category.handler)(project)
    handler.to_easydata(project_id=project_id, **{k: connexion.request.json[k] for k in ["access_token", "dataset_id"]})


def split_dataset(project_id):
    Project._exists(project_id)
    split = connexion.request.json
    if list(split.keys()) != ["train", "val", "test"]:
        abort(
            f"Got {split}",
            500,
            "Request should provide train, validataion and test percentage",
        )
    if sum(split.values()) != 100:
        abort(
            f"The train({split['train']}), val({split['val']}), test({split['test']}) split don't sum to 100.",
            500,
            "The three percentages don't sum to 100",
        )
    split_num = [0] * 3
    split_num[1] = split["train"] / 100
    split_num[2] = split["val"] / 100
    split = split_num

    for idx in range(1, 3):
        split[idx] += split[idx - 1]

    tasks = Task._get(project_id=project_id, many=True)
    split = [math.ceil(s * len(tasks)) for s in split]
    split.append(len(tasks))

    random.shuffle(tasks)
    for set_idx in range(3):
        for idx in range(split[set_idx], split[set_idx + 1]):
            tasks[idx].set = set_idx
    db.session.commit()
    tasks = Task._get(project_id=project_id, many=True)
    return {
        "train": split[1],
        "val": split[2] - split[1],
        "test": split[3] - split[2],
    }, 200


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


def import_options(project_type):
    all_catgs = TaskCategory._get(many=True)
    assert project_type in [c.name for c in all_catgs], f"Project type specified {project_type} isn't supported"
    selector = eval(f"paddlelabel.task.{project_type}.ProjectSubtypeSelector")()
    print(selector.questions)
