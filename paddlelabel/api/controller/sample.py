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
        "bear/placeholder/1/1.jpeg",
        "bear/placeholder/2/2.jpeg",
        "bear/placeholder/3/3.jpeg",
        "bear/placeholder/4/4.jpeg",
        "bear/classification/multiClass/image/1.jpeg",
        "bear/classification/multiClass/image/2.jpeg",
        "bear/classification/multiClass/image/3.jpeg",
        "bear/classification/multiClass/image/4.jpeg",
        "bear/classification/singleClass/1/1.jpeg",
        "bear/classification/singleClass/2/2.jpeg",
        "bear/classification/singleClass/3/3.jpeg",
        "bear/classification/singleClass/4/4.jpeg",
        "bear/detection/coco/JPEGImages/1.jpeg",
        "bear/detection/coco/JPEGImages/2.jpeg",
        "bear/detection/coco/JPEGImages/3.jpeg",
        "bear/detection/coco/JPEGImages/4.jpeg",
        "bear/detection/voc/JPEGImages/1.jpeg",
        "bear/detection/voc/JPEGImages/2.jpeg",
        "bear/detection/voc/JPEGImages/3.jpeg",
        "bear/detection/voc/JPEGImages/4.jpeg",
        "bear/img/1.jpeg",
        "bear/img/2.jpeg",
        "bear/img/3.jpeg",
        "bear/img/4.jpeg",
        "bear/instanceSegmentation/mask/JPEGImages/1.jpeg",
        "bear/instanceSegmentation/mask/JPEGImages/2.jpeg",
        "bear/instanceSegmentation/mask/JPEGImages/3.jpeg",
        "bear/instanceSegmentation/mask/JPEGImages/4.jpeg",
        "bear/instanceSegmentation/polygon/image/1.jpeg",
        "bear/instanceSegmentation/polygon/image/2.jpeg",
        "bear/instanceSegmentation/polygon/image/3.jpeg",
        "bear/instanceSegmentation/polygon/image/4.jpeg",
        "bear/semanticSegmentation/mask/JPEGImages/1.jpeg",
        "bear/semanticSegmentation/mask/JPEGImages/2.jpeg",
        "bear/semanticSegmentation/mask/JPEGImages/3.jpeg",
        "bear/semanticSegmentation/mask/JPEGImages/4.jpeg",
        "bear/semanticSegmentation/polygon/image/1.jpeg",
        "bear/semanticSegmentation/polygon/image/2.jpeg",
        "bear/semanticSegmentation/polygon/image/3.jpeg",
        "bear/semanticSegmentation/polygon/image/4.jpeg",
        "fruit/classification/multiClass/image/1.jpeg",
        "fruit/classification/multiClass/image/2.jpeg",
        "fruit/classification/multiClass/image/3.jpeg",
        "fruit/classification/multiClass/image/4.jpeg",
        "fruit/classification/multiClass/image/5.jpeg",
        "fruit/placeholder/梨/2.jpeg",
        "fruit/placeholder/梨/4.jpeg",
        "fruit/placeholder/苹果/1.jpeg",
        "fruit/placeholder/苹果/3.jpeg",
        "fruit/classification/singleClass/梨/2.jpeg",
        "fruit/classification/singleClass/梨/4.jpeg",
        "fruit/classification/singleClass/苹果/1.jpeg",
        "fruit/classification/singleClass/苹果/3.jpeg",
        "fruit/classification/singleClass/5.jpeg",
        "fruit/detection/coco/image/1.jpeg",
        "fruit/detection/coco/image/2.jpeg",
        "fruit/detection/coco/image/3.jpeg",
        "fruit/detection/coco/image/4.jpeg",
        "fruit/detection/coco/image/5.jpeg",
        "fruit/detection/voc/JPEGImages/1.jpeg",
        "fruit/detection/voc/JPEGImages/2.jpeg",
        "fruit/detection/voc/JPEGImages/3.jpeg",
        "fruit/detection/voc/JPEGImages/4.jpeg",
        "fruit/detection/voc/JPEGImages/5.jpeg",
        "fruit/img/1.jpeg",
        "fruit/img/2.jpeg",
        "fruit/img/3.jpeg",
        "fruit/img/4.jpeg",
        "fruit/img/5.jpeg",
        "fruit/instanceSegmentation/mask/JPEGImages/1.jpeg",
        "fruit/instanceSegmentation/mask/JPEGImages/2.jpeg",
        "fruit/instanceSegmentation/mask/JPEGImages/3.jpeg",
        "fruit/instanceSegmentation/mask/JPEGImages/4.jpeg",
        "fruit/instanceSegmentation/mask/JPEGImages/5.jpeg",
        "fruit/instanceSegmentation/polygon/image/1.jpeg",
        "fruit/instanceSegmentation/polygon/image/2.jpeg",
        "fruit/instanceSegmentation/polygon/image/3.jpeg",
        "fruit/instanceSegmentation/polygon/image/4.jpeg",
        "fruit/instanceSegmentation/polygon/image/5.jpeg",
        "fruit/semanticSegmentation/mask/JPEGImages/1.jpeg",
        "fruit/semanticSegmentation/mask/JPEGImages/2.jpeg",
        "fruit/semanticSegmentation/mask/JPEGImages/3.jpeg",
        "fruit/semanticSegmentation/mask/JPEGImages/4.jpeg",
        "fruit/semanticSegmentation/mask/JPEGImages/5.jpeg",
        "fruit/semanticSegmentation/polygon/image/1.jpeg",
        "fruit/semanticSegmentation/polygon/image/2.jpeg",
        "fruit/semanticSegmentation/polygon/image/3.jpeg",
        "fruit/semanticSegmentation/polygon/image/4.jpeg",
        "fruit/semanticSegmentation/polygon/image/5.jpeg",
    ]
    for dst in dsts:
        img_fdr = osp.join(sample_source, dst.split("/")[0], "img")
        dst = osp.join(sample_dst, dst)
        src = osp.join(img_fdr, osp.basename(dst))
        copy(src, dst, make_dir=True)


def load_sample(sample_family="bear"):
    prep_samples()

    task_category_id = connexion.request.json.get("task_category_id")

    sample_folder = {
        "classification": ["classification", "singleClass"],
        "detection": ["detection", "voc"],
        "semantic_segmentation": ["semanticSegmentation", "mask"],
        "instance_segmentation": ["instanceSegmentation", "polygon"],
    }
    label_formats = {
        "classification": "single_class",
        "detection": "voc",
        "semantic_segmentation": "mask",
        "instance_segmentation": "polygon",
    }
    task_category = TaskCategory._get(task_category_id=task_category_id)
    data_dir = osp.join(
        osp.expanduser("~"), ".paddlelabel", "sample", sample_family, *sample_folder[task_category.name]
    )
    curr_project = Project._get(data_dir=data_dir)
    if curr_project is not None:
        return {"project_id": curr_project.project_id}, 200

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

    return {"project_id": handler.project.project_id}, 200


def sample_folder_structure(path):
    # path = connexion.request.args['path']
    base_path = osp.join(osp.expanduser("~"), ".paddlelabel")
    path.replace("/", osp.sep)
    path = osp.join(base_path, path)

    def dfs(path):
        res = []
        names = os.listdir(path)
        for name in names:
            if name == "paddlelabel.warning":
                continue
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

    file_name = osp.basename(path)
    folder = osp.dirname(path)
    return flask.send_from_directory(folder, file_name)
