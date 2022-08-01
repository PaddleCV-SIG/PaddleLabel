import os
import os.path as osp
import json
from collections import deque

import cv2

from paddlelabel.api import Annotation, Data, Label, Project, Task
from paddlelabel.api.util import abort
from paddlelabel.config import db
from paddlelabel.task.util import image_extensions, listdir, create_dir
from paddlelabel.task.util.color import rgb_to_hex, rand_hex_color, name_to_hex

"""
Base for import/export and other task specific operations.
"""


class BaseTask:
    def __init__(self, project, skip_label_import=False, data_dir=None):
        """
        Args:
            project (int|dict): If the project exists, self.project will be queried from db with parameter project as project_id or with project.project_id. Else the project will be created.
        """

        # 1. set project
        if isinstance(project, int):
            curr_project = Project._get(project_id=project)
            if curr_project is None:
                raise RuntimeError(f"No project with project_id {project}")
        else:
            curr_project = Project._get(project_id=project.project_id)
            if curr_project is None:
                db.session.add(project)
                db.session.commit()
                curr_project = project
        self.project = curr_project

        if data_dir is None:
            data_dir = self.project.data_dir

        # os.makedirs(data_dir, exist_ok=True)

        # 2. set current label max id
        # next added label will have id label_max_id+1, so label.id starts from 1
        self.label_max_id = 0
        for label in project.labels:
            self.label_max_id = max(self.label_max_id, label.id)

        # 3. read dataset split
        self.split = self.read_split(data_dir)

        # 4. create labels specified in labels.txt
        if not skip_label_import:
            self.import_labels()

        # 5. polupate label colors
        self.populate_label_colors()

        # 6. get curr datapaths
        # tasks = Task._get(project_id=project.project_id, many=True)
        # self.curr_data_paths = []
        # for task in tasks:
        #     for data in task.datas:
        #         self.curr_data_paths.append(data.path)
        # print("Current data paths", self.curr_data_paths)

        self.project = Project._get(project_id=project.project_id)

    def add_task(self, datas: list, annotations: list = None, split: int = None):
        """Add one task to project.
        ATTENTION: to be more efficient, this method WONT connmit! make sure you invoke db.session.commit() after adding all tasks

        Parameters
        ----------
        datas : list. each item is a dict, path is required, specifying full or relative path to project.data_dir. Others are optional
            [{"path": 'path1'}, {"path" : 'path2', "size": [1024, 768, 3]}, ...]
        annotations : list
            [
                [ // labels for path1
                    {
                        "label_name": "",
                        "result": "", // optional, default to ""
                    },
                    {
                        "label_name": "",
                        "result": "",
                    }
                ],
                [ // labels for path2
                    {
                        "label_name": "",
                        "result": "", // optional, default to ""
                    },
                    {
                        "label_name": "",
                        "result": "", // optional, default to ""
                    }
                ],
                ...
            ]
        split: int. the split set this task is in. If not passed will attempt to find in the three list files. If not found default to 0 (training set). 0, 1, 2-> train, val, test
        """
        project = self.project
        assert len(datas) != 0, "can't add task without data"
        # print(datas, project.data_dir)

        for idx in range(len(datas)):
            if osp.isabs(datas[idx]["path"]):
                datas[idx]["path"] = osp.relpath(datas[idx]["path"], project.data_dir)

        # 1. find task split
        if split is None:
            split_idx = 0
            for idx, split in enumerate(self.split):
                if datas[0]["path"] in split:
                    split_idx = idx
                    break
        else:
            split_idx = split

        task = Task(project_id=project.project_id, set=split_idx)

        def get_label(name):
            for lab in project.labels:
                if lab.name == name:
                    return lab
            return None

        if annotations is None:
            annotations = []
        while len(annotations) < len(datas):
            annotations.append([])

        for anns, data_record in zip(annotations, datas):
            # 2. add data record
            data = Data(**data_record)
            task.datas.append(data)
            total_anns = 0

            # 3. add data's annotations
            for ann in anns:
                if len(ann.get("label_name", "")) == 0:
                    continue
                # BUG: multiple labels under same label_name can exist
                label = get_label(ann["label_name"])
                if label is None:
                    label = self.add_label(ann["label_name"], ann.get("color"), commit=True)
                del ann["label_name"]
                ann = Annotation(label_id=label.label_id, project_id=project.project_id, **ann)
                task.annotations.append(ann)  # TODO: remove
                data.annotations.append(ann)
                total_anns += 1
            print(f"==== {data_record['path']} with {total_anns} annotation(s) imported to set {split_idx} ====")

        db.session.add(task)

    def label_id2name(self, label_id):
        for label in self.project.labels:
            if label.id == label_id:
                return label.name
        return None

    def label_name2id(self, label_name):
        for label in self.project.labels:
            if label.name == label_name:
                return label.id
        return None

    def label_name2label_id(self, label_name):
        for label in self.project.labels:
            if label.name == label_name:
                return label.label_id
        return None

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

    def export_split(
        self,
        export_dir,
        tasks,
        new_paths,
        delimiter=" ",
        with_labels=True,
        annotation_ext=None,
    ):
        # only used in file-file split, not in file-class split
        if annotation_ext is not None and annotation_ext[0] == ".":
            annotation_ext = annotation_ext[1:]

        set_names = ["train_list", "val_list", "test_list"]
        create_dir(export_dir)
        set_files = [open(osp.join(export_dir, f"{n}.txt"), "w") for n in set_names]
        for task, task_new_paths in zip(tasks, new_paths):
            for data, new_path in zip(task.datas, task_new_paths):
                if with_labels:
                    label_ids = []
                    for ann in data.annotations:
                        label_ids.append(ann.label.id - 1)
                    if len(label_ids) == 0:
                        continue
                    label_ids = [str(id) for id in label_ids]
                    print(
                        new_path + delimiter + delimiter.join(label_ids),
                        file=set_files[task.set],
                    )
                else:
                    annotation_path = new_path.replace("JPEGImages", "Annotations")
                    annotation_path = annotation_path[: -annotation_path[::-1].find(".")] + annotation_ext
                    print(new_path + delimiter + annotation_path, file=set_files[task.set])

        for f in set_files:
            f.close()

    """ label related """

    def add_label(
        self,
        name: str,
        id: int = None,
        color: str = None,
        super_category_id: int = None,
        comment: str = None,
        commit=False,
    ):
        """
        Add one label to current project

        Args:
            name (str): label name
            id (int, optional): id. Defaults to None, autoincrement.
            color (str, optional): the color this label uses, can be hex color with leading # or name for a common color. will raise runtime error if specified color is in use by other labels. Defaults to None, will randomly generate.
            comment (str, optional): comment for label. Defaults to None.
            super_category_id (int, optional): id of supercategory. Defaults to None.
            commit (bool, optional): True -> commit after adding label. Defaults to False.

        Returns:
            Label: new label generated
        """
        # 1. check params
        if name is None or len(name) == 0:
            raise RuntimeError(f"Label name is required, got {name}")
        current_names = set(l.name for l in self.project.labels)
        if name in current_names:
            # raise RuntimeError(f"Label name {name} is not unique")
            print(f"Label {name} already exist, skipping.")
            return

        # 2. check or assign color
        current_colors = set(l.color for l in self.project.labels)
        if color is None:
            color = rand_hex_color(current_colors)
        else:
            if color[0] != "#":
                color = name_to_hex(color)
            if color in current_colors:
                raise RuntimeError(f"Label color {color} is not unique")

        # 3. check or assign id
        current_ids = set(int(l.id) for l in self.project.labels)
        if id is None:
            id = self.label_max_id + 1
        else:
            id = int(id)
            if id in current_ids:
                raise RuntimeError(f"Label id {id} is not unique")

        # 4. assign super category id

        label = Label(
            project_id=self.project.project_id,
            id=id,
            name=name,
            color=color,
            comment=comment,
            super_category_id=super_category_id,
        )
        self.project.labels.append(label)
        if commit:
            db.session.commit()
        current_ids = [l.id for l in self.project.labels]

        self.label_max_id = max(current_ids)
        return label

    def import_labels(self, delimiter=" ", ignore_first=False):
        # 1. set params
        label_names_path = None
        project = self.project
        if project.other_settings is not None:
            if isinstance(project.other_settings, str):
                other_settings = json.loads(project.other_settings)
            else:
                other_settings = project.other_settings
            label_names_path = other_settings.get("label_names_path", None)

        if label_names_path is None:
            label_names_path = osp.join(project.data_dir, "labels.txt")

        if label_names_path is None or not osp.exists(label_names_path):
            return

        # 2. import labels
        labels = open(label_names_path, "r").readlines()
        labels = [l.strip() for l in labels if len(l.strip()) != 0]
        if ignore_first:
            background_line = labels[0]
            labels = labels[1:]

        labels = [l.split("//") for l in labels]
        comments = [None if len(l) == 1 else l[1].strip() for l in labels]
        labels = [l[0].strip() for l in labels]
        labels = [l.split(delimiter) for l in labels]

        current_labels = Label._get(project_id=self.project.project_id, many=True)
        current_labels = [l.name for l in current_labels]
        for label, comment in zip(labels, comments):
            """
            label length: 1: label name
                          2: label name | label id
                          3: label name | label id | hex color or common color name or grayscale value
                          5: label name | label id | r | g | b color
                          //: string after // is stored as comment
                          -: skip this field
            """
            valid_lengths = [1, 2, 3, 5]
            if len(label) not in valid_lengths:
                raise RuntimeError(f"After split got {label}. It's not in valid lengths {valid_lengths}")
            if label[0] not in current_labels:
                print("==== Adding label", label, "====")
                if len(label) == 5:
                    label[2] = rgb_to_hex(label[2:])
                    del label[3]
                label = [None if v == "-" else v for v in label]
                self.add_label(*label, comment=comment)
        db.session.commit()

        if ignore_first:
            return background_line

    def populate_label_colors(self):
        labels = Label._get(project_id=self.project.project_id, many=True)
        for lab in labels:
            if lab.color is None:
                lab.color = rand_hex_color([l.color for l in labels])
        db.session.commit()

    def export_labels(self, export_dir: str, background_line: str = None, with_id: bool = False):
        label_names_path = osp.join(export_dir, "labels.txt")
        labels = self.project.labels
        labels.sort(key=lambda l: l.id)
        with open(label_names_path, "w") as f:
            if background_line is not None:
                print(background_line.strip(), file=f)
            for lab in labels:
                # print(lab)
                print(lab.name, end=" " if with_id else "\n", file=f)
                if with_id:
                    print(lab.id, file=f)
        return labels

    # TODO: add total imported count
    def default_importer(
        self,
        data_dir=None,
        filters={"exclude_prefix": ["."], "include_postfix": image_extensions},
        with_size=False,
    ):
        if data_dir is None:
            data_dir = self.project.data_dir

        for data_path in listdir(data_dir, filters):
            if with_size:
                img = cv2.imread(osp.join(data_dir, data_path))
                size = [1] + list(img.shape)
                size = ",".join([str(s) for s in size])
                self.add_task([{"path": data_path, "size": size}])
            else:
                self.add_task([{"path": data_path}])
        db.session.commit()

    """ warning file """

    def create_warning(self, dir):
        if not osp.exists(dir):
            abort(detail=f"Dataset Path specified {dir} doesn't exist.", status=404)

        warning_path = osp.join(dir, "paddlelabel.warning")
        if not osp.exists(warning_path):
            print(
                "PP Label is using files stored under this folder!\nChanging file in this folder may cause issues.",
                file=open(warning_path, "w"),
            )

    def remove_warning(self, dir):
        warning_path = osp.join(dir, "paddlelabel.warning")
        if osp.exists(warning_path):
            os.remove(warning_path)

    def create_coco_labels(self, labels):
        catgs = deque()

        for catg in labels:
            catgs.append(catg)

        tried_names = []  # guard against invalid dependency graph
        for _ in range(len(catgs) * 2):
            if len(catgs) == 0:
                break
            catg = catgs.popleft()
            if self.label_name2id(catg["name"]) is not None:
                continue

            color = catg.get("color", None)
            if color is not None:
                color = name_to_hex(color)
            if (
                "supercategory" not in catg.keys()
                or catg["supercategory"] == "none"
                or catg["supercategory"] is None
                or len(catg["supercategory"]) == 0
            ):
                self.add_label(
                    name=catg["name"],
                    id=catg["id"],
                    super_category_id=None,
                    color=color,
                )
            else:
                super_category_id = self.label_name2label_id(catg["supercategory"])
                if super_category_id is None and catg["name"] not in tried_names:
                    catgs.append(catg)
                    tried_names.append(catg["name"])
                else:
                    self.add_label(
                        name=catg["name"],
                        id=catg["id"],
                        super_category_id=super_category_id,
                        color=color,
                    )
            db.session.commit()
