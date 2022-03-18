import os
import os.path as osp
import json
import shutil

from pplabel.config import db
from pplabel.api import Project, Task, Data, Annotation, Label
from pplabel.api.schema import ProjectSchema
from pplabel.api.util import rand_color
from pplabel.task.util import create_dir, listdir, copy

"""
Base for import/export and other task specific operations.
"""


class BaseTask:
    def __init__(self, project):
        """
        Args:
            project (int|dict): If the project exists, pass in project_id, else pass in a dict containing project info (either case labels will be queried from db).
        """
        if isinstance(project, int):
            curr_project = Project._get(project_id=project)
            if curr_project is None:
                raise RuntimeError(f"No project with project_id {project}")
        else:
            curr_project = Project._get(project_id=project.project_id)
            if curr_project is None:
                db.session.add(project)
                db.session.commit()
        self.project = curr_project
        label_max_id = 0
        for label in project.labels:
            label_max_id = max(label_max_id, label.id)
        self.label_max_id = label_max_id

    def add_label(self, name: str, color: str):
        if color is None:
            color = rand_color([l.color for l in self.project.labels])
        label = Label(
            id=self.label_max_id + 1,
            project_id=self.project.project_id,
            name=name,
            color=color,
        )
        self.project.labels.append(label)
        db.session.commit()
        self.label_max_id += 1
        return label

    def add_task(self, data_paths: list, annotations: list):
        """Add one task to project.

        Parameters
        ----------
        data_paths : list. each path should either be full path or relative path to project.data_dir
            ['path1', 'path2', ...]
        annotations : list
            [
                [ // labels for path1
                    {
                        "label_name": "",
                        "result": "", // optional, default to ""
                        "color": "" // optional, new label will be given a randon color
                    },
                    {
                        "label_name": "",
                        "result": "",
                        "color": ""
                    }
                ],
                [ // labels for path2
                    {
                        "label_name": "",
                        "result": "", [optional, default to ""]
                        "color": ""
                    },
                    {
                        "label_name": "",
                        "result": "", [optional, default to ""]
                        "color": ""
                    }
                ],
                ...
            ]
        """
        project = self.project
        task = Task(project_id=project.project_id)

        def getLabel(name):
            for lab in project.labels:
                if lab.name == name:
                    return lab
            return None

        for anns, data_path in zip(annotations, data_paths):
            # 1. add data record
            if project.data_dir in data_path:
                data_path = osp.relpath(data_path, project.data_dir)
            data = Data(path=data_path, slice_count=1)  # TODO: generate slice_count from io
            task.datas.append(data)

            # 2. add data's annotations
            for ann in anns:
                label = getLabel(ann["label_name"])
                print("0-0-0-0-0", label)
                if label is None:
                    label = self.add_label(ann["label_name"], ann.get("color"))
                ann = Annotation(
                    label_id=label.label_id,
                    project_id=project.project_id,
                    result=ann.get("result", ""),
                )
                task.annotations.append(ann)
                data.annotations.append(ann)

        db.session.add(task)
        db.session.commit()
