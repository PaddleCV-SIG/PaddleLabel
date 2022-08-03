import os
import os.path as osp
import requests
import tarfile
import zipfile
from pathlib import Path

from tqdm import tqdm
import connexion
import flask

import paddlelabel
from paddlelabel.config import data_base_dir
from paddlelabel.api.schema import ProjectSchema
from paddlelabel.api.model import TaskCategory, Project
from paddlelabel.api.util import abort
from paddlelabel.config import basedir
from paddlelabel.task.util.file import copy, copycontent


def prep_samples(sample_dst: str = None):
    if sample_dst is None:
        sample_dst = osp.join(osp.expanduser("~"), ".paddlelabel", "sample")
    sample_source = osp.join(basedir, "sample")
    copycontent(sample_source, sample_dst)

    dsts = [
        "clas/multi/image/1.jpeg",
        "clas/multi/image/2.jpeg",
        "clas/multi/image/3.jpeg",
        "clas/multi/image/4.jpeg",
        "clas/single/1/1.jpeg",
        "clas/single/2/2.jpeg",
        "clas/single/3/3.jpeg",
        "clas/single/4/4.jpeg",
        "det/coco/JPEGImages/1.jpeg",
        "det/coco/JPEGImages/2.jpeg",
        "det/coco/JPEGImages/3.jpeg",
        "det/coco/JPEGImages/4.jpeg",
        "det/voc/JPEGImages/1.jpeg",
        "det/voc/JPEGImages/2.jpeg",
        "det/voc/JPEGImages/3.jpeg",
        "det/voc/JPEGImages/4.jpeg",
        "instance_seg/mask/JPEGImages/1.jpeg",
        "instance_seg/mask/JPEGImages/2.jpeg",
        "instance_seg/mask/JPEGImages/3.jpeg",
        "instance_seg/mask/JPEGImages/4.jpeg",
        "instance_seg/polygon/image/1.jpeg",
        "instance_seg/polygon/image/2.jpeg",
        "instance_seg/polygon/image/3.jpeg",
        "instance_seg/polygon/image/4.jpeg",
        "semantic_seg/mask/JPEGImages/1.jpeg",
        "semantic_seg/mask/JPEGImages/2.jpeg",
        "semantic_seg/mask/JPEGImages/3.jpeg",
        "semantic_seg/mask/JPEGImages/4.jpeg",
        "semantic_seg/polygon/image/1.jpeg",
        "semantic_seg/polygon/image/2.jpeg",
        "semantic_seg/polygon/image/3.jpeg",
        "semantic_seg/polygon/image/4.jpeg",
    ]
    img_path = osp.join(sample_source, "imgs")
    for dst in dsts:
        dst = osp.join(sample_dst, dst)
        src = osp.join(img_path, osp.basename(dst))
        copy(src, dst, make_dir=True)


def load_sample():
    prep_samples()

    task_category_id = connexion.request.json.get("task_category_id")

    sample_folder = {
        "classification": ["clas", "single"],
        "detection": ["det", "voc"],
        "semantic_segmentation": ["semantic_seg", "mask"],
        "instance_segmentation": ["instance_seg", "polygon"],
    }
    label_formats = {
        "classification": "single_class",
        "detection": "voc",
        "semantic_segmentation": "mask",
        "instance_segmentation": "polygon",
    }
    task_category = TaskCategory._get(task_category_id=task_category_id)
    data_dir = osp.join(osp.expanduser("~"), ".paddlelabel", "sample", *sample_folder[task_category.name])
    curr_project = Project._get(data_dir=data_dir)
    if curr_project is not None:
        # abort(f"Sample project for {task_category.name} is already created. Please visit home page to enter the project.", 500)
        return {"project_id": curr_project.project_id}, 200

    # print(task_category.name, task_category)

    project = {
        "name": f"Sample Project - {task_category.name}",
        "description": f"A {task_category.name} sample project created by PP-Label",
        "task_category_id": str(task_category_id),
        "data_dir": data_dir,
        "label_format": label_formats[task_category.name],
    }
    project = ProjectSchema().load(project)

    if task_category is None:
        handler = paddlelabel.task.BaseTask(project)
    else:
        handler = eval(task_category.handler)(project, data_dir=data_dir)

    handler.default_importer()

    # print(handler.project)

    return {"project_id": handler.project.project_id}, 200


def sample_folder_structure(path):
    # path = connexion.request.args['path']
    base_path = osp.join(osp.join(osp.expanduser("~"), ".paddlelabel", "sample"))
    path.replace("/", osp.sep)
    path = osp.join(base_path, path)
    print(path)

    def dfs(path):
        res = []
        names = os.listdir(path)
        for name in names:
            temp = {}
            full_path = osp.join(path, name)
            if osp.isdir(full_path):
                temp["title"] = name
                temp["key"] = osp.relpath(full_path, base_path)
                temp["children"] = dfs(full_path)
            else:
                temp["title"] = name
                temp["key"] = osp.relpath(full_path, base_path)
                temp["isLeaf"] = True
            res.append(temp)
        # res.sort()
        return res

    res = dfs(path)

    return res, 200


def serve_sample_file(path):
    base_path = osp.join(osp.join(osp.expanduser("~"), ".paddlelabel", "sample"))
    path.replace("/", osp.sep)
    path = osp.join(base_path, path)
    print(path)

    file_name = osp.basename(path)
    folder = osp.dirname(path)
    print(folder, file_name)
    return flask.send_from_directory(folder, file_name)
