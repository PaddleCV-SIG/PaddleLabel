import os.path as osp

from pplabel.api import Annotation, Data, Label, Project, Task
from pplabel.api.util import rand_color
from pplabel.config import db
from pplabel.task.util import image_extensions, listdir

"""
Base for import/export and other task specific operations.
"""


class BaseTask:
    def __init__(self, project):
        """
        Args:
            project (int|dict): If the project exists, self.project will be queried from db with parameter project or project.project_id. Else the project with parameter project as info will be created.
        """

        # 1. set project
        if isinstance(project, int):
            curr_project = Project._get(project_id=project)
            if curr_project is None:
                raise RuntimeError(f"No project with project_id {project} found")
        else:
            curr_project = Project._get(project_id=project.project_id)
            if curr_project is None:
                db.session.add(project)
                db.session.commit()
        self.project = curr_project

        # 2. set max label id
        label_max_id = 0
        for label in project.labels:
            label_max_id = max(label_max_id, label.id)
        self.label_max_id = label_max_id

        # 3. generate random color for labels if not set
        for lab in self.project.labels:
            if lab.color is None:
                lab.color = rand_color([l.color for l in self.project.labels])
        db.session.commit()

        # 4. read split
        self.split = self.read_split()

    def add_label(self, name: str, color: str = None):
        if name is None or len(name) == 0:
            return
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

    def add_task(self, data_paths: list, annotations: list = None, split: int = None):
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
        split: int. the split set this task is in. If not passed will attempt to find in the three list files. If not found default to 1 (training set).
        """
        project = self.project
        assert len(data_paths) != 0, "can't add task without data"

        # 1. find task split
        # ensure all relative paths
        for idx, data_path in enumerate(data_paths):
            if project.data_dir in data_path:
                data_paths[idx] = osp.relpath(data_path, project.data_dir)

        split_idx = 0
        for idx, split in enumerate(self.split):
            if data_paths[0] in split:
                split_idx = idx
                break
        task = Task(project_id=project.project_id, set=split_idx)

        def get_label(name):
            for lab in project.labels:
                if lab.name == name:
                    return lab
            return None

        if annotations is None or len(annotations) == 0:
            annotations = [[]] * len(data_paths)
        for anns, data_path in zip(annotations, data_paths):
            # 2. add data record
            data = Data(path=data_path, slice_count=1)  # TODO: generate slice_count from io
            task.datas.append(data)

            # 3. add data's annotations
            for ann in anns:
                if ann is None or len(ann.get("label_name", "")) == 0:
                    continue
                # BUG: multiple labels under same label_name can exist
                label = get_label(ann["label_name"])
                if label is None:
                    label = self.add_label(ann["label_name"], ann.get("color"))
                ann = Annotation(
                    label_id=label.label_id,
                    project_id=project.project_id,
                    result=ann.get("result", ""),
                )
                task.annotations.append(ann)
                data.annotations.append(ann)
            print(
                f"==== {data_path} with {len(anns)} annotation{'' if len(anns)==1 else 's'} imported to set {split_idx} ===="
            )

        db.session.add(task)
        db.session.commit()

    # TODO: add total imported count
    def default_importer(
        self, data_dir=None, filters={"exclude_prefix": ["."], "include_postfix": image_extensions}
    ):
        if data_dir is None:
            data_dir = self.project.data_dir

        for data_path in listdir(data_dir, filters):
            self.add_task([data_path])

    def read_split(self, data_dir=None, delimiter=" "):
        if data_dir is None:
            data_dir = self.project.data_dir

        sets = []
        split_names = ["train_list.txt", "val_list.txt", "test_list.txt"]
        for split_name in split_names:
            split_path = osp.join(data_dir, split_name)
            paths = []
            if osp.exists(split_path):
                paths = open(split_path, "r").readlines()
                paths = [p.strip() for p in paths if len(p.strip()) != 0]
                paths = [p.split(delimiter)[0] for p in paths]
            sets.append(set(paths))
        return sets

    def write_split(self, export_dir, tasks=None, delimiter=" "):
        if tasks is None:
            tasks = Task._get(project_id=self.project.project_id, many=True)

        set_names = ["train", "val", "test"]
        set_files = [open(osp.join(export_dir, f"{n}.txt"), "w") for n in set_names]
        for task in tasks:
            for data in task.datas:
                label_ids = []
                for ann in data.annotations:
                    label_ids.append(ann.label.id)
                label_ids = [str(id) for id in label_ids]
                print(data.path + delimiter + delimiter.join(label_ids), file=set_files[task.set])

        for f in set_files:
            f.close()
