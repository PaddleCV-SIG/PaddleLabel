# -*- coding: utf-8 -*-
from __future__ import annotations

import logging
import os.path as osp  # TODO: remove
from collections import deque
from pathlib import Path

from paddlelabel.api import Annotation, Data, Label, Project, Task
from paddlelabel.config import db
from paddlelabel.task.util import create_dir, image_extensions, listdir
from paddlelabel.task.util.color import name_to_hex, rand_hex_color, rgb_to_hex
from paddlelabel.io.image import getSize

"""
Base for import/export and other task specific operations.
"""

logger = logging.getLogger("paddlelabel")

# TODO: change data_dir to pathlib.path
class BaseTask:
    def __init__(
        self,
        project: int | Project,
        data_dir: None | Path = None,
        skip_label_import: bool = False,
        is_export: bool = False,
    ):
        """Basic import/export related operations

        Parameters
        ----------
        project : int | Project
            If the project exists in db, self.project will be queried from db with parameter project(int) as project_id or with project.project_id. Else the project will be created. # TODO: can we change this to only accept project_id
        data_dir : None | str, optional
            Base path to dataset. If it's None, will use project.data_dir. Defaults to False.
        skip_label_import : bool, optional
            If false, will attempt to import labels from data_dir/labels.txt. Defaults to False.
        is_export : bool, optional
            If this class instance will be used for export. If True, some default import functions won't run. Defaults to False

        Raises
        ------
        RuntimeError
            Project with given project_id not found.
        """

        self.task_cache: list[Task] = []

        # 1. set project
        if isinstance(project, int):
            project = Project._get(project_id=project)
            if project is None:
                raise RuntimeError(f"No project with project_id {project}")
        else:
            res = Project._get(project_id=project.project_id)
            if res is None:
                db.session.add(project)
                db.session.commit()

        self.project = project
        self.project.data_dir = self.project.data_dir.strip()
        db.session.commit()

        if data_dir is None:
            data_dir = self.project.data_dir
        assert data_dir is not None and Path().exists()

        # 2. set current label max id
        # next added label will have id label_max_id+1, so label.id starts from 1
        self.label_max_id = 0
        for label in self.project.labels:
            self.label_max_id = max(self.label_max_id, label.id)

        # 3. read dataset split
        if not is_export:
            self.split = self.read_split()

        # 4. create labels specified in labels.txt
        if not skip_label_import and not is_export:
            self.import_labels()

        # 5. populate label colors
        self.populate_label_colors()

        # TODO: remove after v1.0
        # 6. get curr datapaths
        # tasks = Task._get(project_id=project.project_id, many=True)
        # self.curr_data_paths = []
        # for task in tasks:
        #     for data in task.datas:
        #         self.curr_data_paths.append(data.path)
        # print("Current data paths", self.curr_data_paths)

        # TODO: is this query really needed?
        # self.project = Project._get(project_id=project.project_id)
        # assert isinstance(self.project, Project)

    def add_task(
        self,
        datas: list[dict[str, str | None]],
        annotations: list[list[dict[str, str]]] | None = None,
        split: int | None = None,
    ):
        """
        Cache one task to be written to db later.
        ATTENTION: This method NEVER writes to db! Call commit() to write results to db

        Parameters
        ----------
        datas : list[dict]
            A list of dict, each dict representing a task. In the dict, path is required, specifying full path or relative path to project.data_dir. All other entries are optional.
            Example: [{"path": 'path1'}, {"path" : 'path2', "size": "1,1024,768"}, ...]
            size is in format "slice count (1 for 2d images),height,width" no spaces in the str
        annotations : list[list[dict]] | None, optional
            Annotations corresponding to each data record. Defaults to None
            Example:
                [
                    [ // annotations for path1
                        {
                            "label_name": "",
                            "result": "", // optional, default to ""
                        },
                        {
                            "label_name": "",
                        }
                    ],
                    [ // annotations for path2
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
        split : int | None, optional
            The subset these data records belong to.
            0, 1, 2 -> train, validation, test.
            If not passed, will try to determine from xx_list.txt files.
            If not found, defaults to training subset.
            Defaults to None
        """

        project = self.project
        assert len(datas) != 0, "Can't add task without data"

        for idx, data in enumerate(datas):
            if osp.isabs(datas[idx]["path"]):
                datas[idx]["path"] = osp.relpath(datas[idx]["path"], project.data_dir)
            datas[idx]["path"] = str(datas[idx]["path"])

        # 1. find task split
        if split is None:
            split_idx = 0
            for idx, split_paths in enumerate(self.split):
                if datas[0]["path"] in split_paths:
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

        for anns, data in zip(annotations, datas):
            # 2. add data record
            data = Data(**data)
            task.datas.append(data)
            total_anns = 0

            # 3. add data's annotations
            for ann in anns:
                if len(ann.get("label_name", "")) == 0:
                    continue
                label = get_label(ann["label_name"])
                if label is None:
                    label = self.add_label(ann["label_name"], ann.get("color"), commit=True)
                del ann["label_name"]
                ann = Annotation(label_id=label.label_id, project_id=project.project_id, **ann)
                task.annotations.append(ann)  # TODO: remove this, annotation should only be under data
                data.annotations.append(ann)
                total_anns += 1
            logger.debug(f"{data.path} with {total_anns} annotation(s) under set {split_idx} discovered")

        self.task_cache.append(task)

    def commit(self):
        """Write cached tasks to database, ordered by filename."""
        self.task_cache.sort(key=lambda k: k.datas[0].path)
        for task in self.task_cache:
            db.session.add(task)
        logger.info(
            f"{len(self.task_cache)} tasks and {sum(len(t.annotations) for t in self.task_cache)} annotations imported"
        )
        self.task_cache = []
        db.session.commit()

    # TODO: change following three to get_label_by_xx
    def label_id2name(self, label_id: int | float):
        """
        Get label name by label.id
        ATTENTION: label.id, not label.label_id

        Args:
            label_id (int | float): label.id

        Returns:
            str: label_name. None if not found
        """
        label_id = int(label_id)
        for label in self.project.labels:
            # print("++", label.id, label_id)
            if label.id == label_id:
                return label.name
        return None

    def label_name2id(self, label_name: str):
        for label in self.project.labels:
            if label.name == label_name:
                return label.id
        return None

    def label_name2label_id(self, label_name: str):
        for label in self.project.labels:
            if label.name == label_name:
                return label.label_id
        return None

    def read_split(self, separator: str = " ") -> list[set[str]]:
        """
        Read the dataset split information from project.data_dir/xx_list.txt files.

        Parameters
        ----------
        delimiter : str, optional
            The delimiter used in xx_list.txt files. Defaults to " "

        Returns
        -------
        list[set[str]]
            A list of three sets, each set containing all the paths of data in this set.
        """
        data_dir = Path(self.project.data_dir)

        sets: list[set[str]] = []
        split_names = ["train_list.txt", "val_list.txt", "test_list.txt"]
        for split_name in split_names:
            split_path = data_dir / split_name
            if split_path.exists():
                paths = split_path.read_text(encoding="utf-8").split("\n")
                paths = [p.strip().split(separator)[0] for p in paths if len(p.strip()) != 0]
            else:
                paths = []
            sets.append(set(paths))
        return sets

    def export_split(
        self,
        export_dir: Path,
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
        set_files = [open(osp.join(export_dir, f"{n}.txt"), "w", encoding="utf-8") for n in set_names]
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
        id: int | None = None,
        color: str | None = None,
        super_category_id: int | None = None,
        comment: str | None = None,
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
        name = name.strip()
        current_names = set(l.name for l in self.project.labels)
        if name in current_names:
            # raise RuntimeError(f"Label name {name} is not unique")
            raise RuntimeError(f"Trying to add label {name} which already exists.")

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
            name=name.replace(" ", "_"),
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

    def import_labels(self, delimiter: str = " ", ignore_first: bool = False):
        # 1. set params
        label_names_path = None
        project = self.project
        data_dir = Path(project.data_dir)
        # 1.1 try project.data_dir / "labels.txt"
        label_names_path = data_dir / "labels.txt"
        # 1.2 if labels.txt doesn't exist, try: searching for classes.names.
        # NOTE: This is intended for yolo format
        if not label_names_path.exists():
            classes_path = listdir(data_dir, exact_match_one_of=["classes.txt", "classes.names"])
            if len(classes_path) == 0:
                return
            if len(classes_path) > 1:
                logger.error(f"Found {len(classes_path)} classes files at {','.join(classes_path)}")
                return
            label_names_path = data_dir / classes_path[0]
        # 1.3 if label file doesn't exist, there's nothing to import
        if not label_names_path.exists():
            return

        # 2. import labels
        labels = label_names_path.read_text(encoding="utf-8").split("\n")
        # labels = Path(label_names_path).read_text().split("\n")
        labels = [l.strip() for l in labels if len(l.strip()) != 0]

        # 2.1 ignore first background label
        background_line = labels[0]
        if ignore_first:
            labels = labels[1:]

        # 2.2 parse labels
        labels = [l.split("//") for l in labels]
        comments = [None if len(l) == 1 else l[1].strip() for l in labels]
        labels = [l[0].strip().split(delimiter) for l in labels]

        current_labels = Label._get(project_id=project.project_id, many=True)
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
                logger.debug(f"Adding label {label}")
                if len(label) == 5:
                    label[2] = rgb_to_hex(label[2:])
                    del label[3]
                label = [None if v == "-" else v for v in label]
                if len(label) > 1 and label[1] is not None:
                    try:
                        int(label[1])
                    except ValueError:
                        raise RuntimeError(
                            f"Got '{label[1]}' as label id which should be a number. PaddleLabel expects label name to be written before label id. e.g: 'Cat 1' is accepted, while '1 Cat' isn't"
                        )
                self.add_label(*label, comment=comment)
        db.session.commit()

        if ignore_first:
            return background_line

    def populate_label_colors(self):
        """
        Assign a color for all labels that don't yet have one
        """
        labels = Label._get(project_id=self.project.project_id, many=True)
        for lab in labels:
            if lab.color is None:
                lab.color = rand_hex_color([l.color for l in labels])
        db.session.commit()

    def export_labels(
        self,
        label_names_path: str,
        background_line: str | None = None,
        with_id: bool = False,
    ) -> dict[int, int]:
        labels = self.project.labels
        labels.sort(key=lambda l: l.id)
        id_mapping = {}
        curr_id = 0
        with open(label_names_path, "w", encoding="utf-8") as f:
            if background_line is not None:
                print(background_line.strip(), file=f)
                curr_id += 1
            for lab in labels:
                print(lab.name, end=" " if with_id else "\n", file=f)
                if with_id:
                    print(lab.id, file=f)
                    id_mapping[lab.id] = lab.id
                else:
                    id_mapping[lab.id] = curr_id
                    curr_id += 1

        return id_mapping

    def default_importer(
        self,
        data_dir: Path | None = None,
        filters={"exclude_prefix": ["."], "include_postfix": image_extensions},
        with_size: bool = True,  # TODO: after result format is changed, default to false
    ):

        data_dir = self.project.data_dir if data_dir is None else data_dir
        assert data_dir is not None

        for data_path in listdir(data_dir, filters):
            if with_size:
                size, _, _ = getSize(Path(data_dir) / data_path)
            else:
                size = None
            self.add_task([{"path": data_path, "size": size}])

        self.commit()

    """ warning file """

    def create_warning(self, data_dir: Path) -> None:
        """
        Create paddlelabel.warning file in data_dir

        Parameters
        ----------
        data_dir : Path
            dataset dir

        Raises
        ------
        FileNotFoundError
            specified data_dir not found

        """
        data_dir = Path(data_dir)
        if not data_dir.exists():
            raise FileNotFoundError(f"Dataset Path specified {data_dir} doesn't exist.")

        warning_path = data_dir / "paddlelabel.warning"
        if not warning_path.exists():
            warning_path.write_text(
                "PP Label is using files stored under this folder!\nChanging file in this folder may cause issues."
            )
            # print(
            #     "PP Label is using files stored under this folder!\nChanging file in this folder may cause issues.",
            #     file=open(warning_path, "w", encoding="utf-8"),
            # )

    def remove_warning(self, data_dir: Path) -> None:
        """
        Remove paddlelabel.warning

        Parameters
        ----------
        data_dir : Path
            Dataset folder path

        Raises
        ------
        FileNotFoundError
            data_dir / "paddlelabel.warning" doesn't exist
        """
        data_dir = Path(data_dir)  # TODO: remove
        (data_dir / "paddlelabel.warning").unlink()

    """ coco utils """

    def create_coco_labels(self, labels):
        catgs = deque()

        for catg in labels:
            catgs.append(catg)

        tried_names = []  # guard against invalid dependency graph
        for _ in range(len(catgs) * 2):
            if len(catgs) == 0:
                break
            catg = catgs.popleft()
            # print(catg, type(catg), dir(catg))
            if self.label_name2id(catg["name"]) is not None:
                continue

            color = catg.get("color", None)
            if color is not None:
                color = rgb_to_hex(color) if isinstance(color, list) else name_to_hex(color)

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
