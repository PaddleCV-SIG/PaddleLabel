import os
import os.path as osp
import json

import pplabel.api
from pplabel.api import Task, Data, Annotation
from pplabel.config import db


def create_dir(path):
    if path is None:
        return False, "Path to create is None"
    if not osp.isabs(path):
        return False, f"Only supports absolute path, got {path}"
    if not osp.isdir(path):
        try:
            os.makedirs(path)
            return True, f"Created directory {path}"
        except Exception as e:
            return False, f"Create {path} failed. Got exception: {e}"
    else:
        return True, f"{path} exists"


def listdir(path, filters={"exclude_prefix": ["."]}):
    files = []
    for root, fdrs, fs in os.walk(path):
        for f in fs:
            files.append(osp.normpath(osp.join(root, f)))
    # TODO: support regx
    include_prefix = filters.get("include_prefix", None)
    include_postfix = filters.get("include_postfix", None)

    def include(path):
        f = osp.basename(path)
        for pref in include_prefix:
            if f[: len(pref)] == pref:
                return True
        for postf in include_postfix:
            if f[-len(postf) :] == postf:
                return True
        return False

    if include_prefix is not None or include_postfix is not None:
        files = list(filter(include, files))

    exclude_prefix = filters.get("exclude_prefix", [])
    exclude_postfix = filters.get("exclude_postfix", [])

    def exclude(path):
        f = osp.basename(path)
        for pref in exclude_prefix:
            if f[: len(pref)] == pref:
                return False
        for postf in exclude_postfix:
            if f[-len(postf) :] == postf:
                return False
        return True

    files = list(filter(exclude, files))
    files.sort()
    files = [osp.normpath(p) for p in files]
    return files


def get_id(path):
    pass


def get_tasks(datas, labels):
    for data in datas:
        # BUG: root dir
        label = osp.basename(osp.dirname(data))
        yield data, [label]


def import_project(project_id, data_dir, label_dir=None, filters={}):
    success, res = create_dir(data_dir)
    if not success:
        return False, res
    data_paths = listdir(data_dir, filters)

    label_paths = []
    if label_dir is not None:
        success, res = create_dir(label_dir)
        if not success:
            return False, res
        label_paths = listdir(label_dir, filters)

    for data_path, label in get_tasks(data_paths, label_paths):
        print(data_path, label)
        task = Task(
            project_id=1,
            datas=[Data(path=data_path)],
            annotations=[Annotation(result=json.dumps(label))],
        )
        task.project_id = 1
        print(task.project_id)
        db.session.add(task)
        # task.datas = [data_path]
        # task.annotations = json.dumps(label)
        db.session.commit()


# import_project(
#     1,
#     "/home/lin/Desktop/data/pplabel/single_clas_toy/PetImages/",
#     filters={"exclude_prefix": ["."], "exclude_postfix": [".db"]},
# )
