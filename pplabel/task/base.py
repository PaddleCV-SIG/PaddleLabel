import os
import os.path as osp
import json
import shutil

from pplabel.config import db
from pplabel.api import Project, Task, Data, Annotation, Label
from pplabel.api.schema import ProjectSchema
from .util import create_dir, listdir, copy, ComponentManager


class BaseTask:
    # NOTE: have to declear these two in subclass

    def __init__(self, project):
        curr_project = Project._get(project_id=project.project_id)
        if curr_project is None:
            db.session.add(project)
            db.session.commit()
        self.project = project
        label_max_id = 0
        labels = self.project.labels
        for label in labels:
            label_max_id = max(label_max_id, label.id)
        self.label_max_id = label_max_id

    def add_task(self, data_paths: list, annotations: list):
        """Add one task to project.

        Parameters
        ----------
        data_paths : list
            ['path1', 'path2']
        annotations : list
            [
                {
                    "label_name": "",
                    "result": "", [optional, default to ""]
                }
            ]
        """
        # TODO: data_path to ann one to many

        project = self.project
        task = Task(
            project_id=project.project_id,
        )
        for ann, data_path in zip(annotations, data_paths):
            # 1. add annotatin
            label = Label._get(name=ann["label_name"], project_id=project.project_id)
            if label is None:
                label = Label(
                    id=self.label_max_id + 1,
                    project_id=project.project_id,
                    name=ann["label_name"],
                )
                project.labels.append(label)
                db.session.commit()
                self.label_max_id += 1
            ann = Annotation(
                label_id=label.label_id,
                project_id=project.project_id,
                # slice_id=ann.get("slice_id", 0),
                result=ann.get("result", ""),
            )
            task.annotations.append(ann)

            if project.data_dir in data_path:
                data_path = osp.relpath(data_path, project.data_dir)
            # TODO: generate slice_count with io
            data = Data(path=data_path, slice_count=1)
            data.annotations.append(ann)
            task.datas.append(data)

        db.session.add(task)
        db.session.commit()
