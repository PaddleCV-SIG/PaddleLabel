# -*- coding: utf-8 -*-
from __future__ import annotations
from functools import partial

from pathlib import Path
import os.path as osp  # TODO: remove this dep
import shutil

from pydantic import validate_arguments

from paddlelabel.api.model import Task, Project
from paddlelabel.task.util import create_dir, listdir, copy, image_extensions
from paddlelabel.task.base import BaseTask


class SingleClass(BaseTask):
    def __init__(self, project, is_export=False):
        super(SingleClass, self).__init__(project, data_dir=project.data_dir, is_export=is_export)
        self.importers = {
            "singleClassFolder": self.folder_importer,
            "singleClassList": self.list_importer,
        }
        self.exporters = {
            "singleClassFolder": self.folder_exporter,
            "singleClassList": self.list_exporter,
        }

    def list_importer(
        self,
        data_dir: Path,
        filters={"exclude_prefix": ["."], "include_postfix": image_extensions},
    ):
        # 1. set params
        data_dir = Path(self.project.data_dir if data_dir is None else data_dir)
        self.create_warning(data_dir)

        # 2. import all datas
        data_paths = [Path(p) for p in listdir(data_dir, filters)]
        list_infos = self.parse_lists(mode="labels")
        # for data_path in data_paths:

        # for data_path in data_paths:
        #     label_name = data_path.parent.name
        #     self.add_task([{"path": str(data_path)}], [[{"label_name": label_name}]])

        self.commit()

    def list_exporter(self, export_dir: Path):
        pass

    def folder_importer(
        self,
        data_dir: Path | None = None,
        filters={"exclude_prefix": ["."], "include_postfix": image_extensions},
    ):
        # 1. set params
        data_dir = Path(self.project.data_dir if data_dir is None else data_dir)
        self.create_warning(data_dir)

        # 2. import all datas
        data_paths = [Path(p) for p in listdir(data_dir, filters)]
        for data_path in data_paths:
            label_name = data_path.parent.name
            self.add_task([{"path": str(data_path)}], [[{"label_name": label_name}]])

        self.commit()

    def folder_exporter(self, export_dir):
        project = self.project
        create_dir(export_dir)
        create_dir(osp.join(export_dir, "no_annotation"))
        have_no_annotation = False

        # 1. write labels.txt
        self.export_labels(osp.join(export_dir, "labels.txt"))

        # 2. create label dirs
        for label in project.labels:
            create_dir(osp.join(export_dir, label.name))

        # 3. move files to output dir
        tasks = Task._get(project_id=project.project_id, many=True)
        new_paths = []
        for task in tasks:
            for data in task.datas:
                label_name = ""
                if len(data.annotations) == 0:
                    label_name = "no_annotation"
                    have_no_annotation = True
                else:
                    label_name = data.annotations[0].label.name
                copy(osp.join(project.data_dir, data.path), osp.join(export_dir, label_name))
                new_paths.append([osp.join(label_name, osp.basename(data.path))])

        if not have_no_annotation:
            shutil.rmtree(osp.join(export_dir, "no_annotation"))

        # 4. write split files
        self.export_split(export_dir, tasks, new_paths)


class MultiClass(BaseTask):
    def __init__(self, project, is_export=False):
        super(MultiClass, self).__init__(project, data_dir=project.data_dir, is_export=is_export)
        self.importers = {}
        self.exporters = {}

    def list_importer(
        self,
        data_dir=None,
        filters={"exclude_prefix": ["."], "include_postfix": image_extensions},
    ):
        # 1. set params
        project = self.project
        if data_dir is None:
            data_dir = project.data_dir
        self.create_warning(data_dir)

        other_settings = self.project._get_other_settings()
        if other_settings is not None:
            delimiter = other_settings.get("xx_list_delimiter", " ")
        else:
            delimiter = " "

        # 2. get label names from xx_list.txt
        label_lines = []
        for list_name in ["train_list.txt", "val_list.txt", "test_list.txt"]:
            list_path = osp.join(data_dir, list_name)
            if osp.exists(list_path):
                label_lines += open(list_path, "r").readlines()
        label_lines = [l.strip().split(delimiter) for l in label_lines if l.strip() != ""]

        labels_dict = {}
        for l in label_lines:
            labs = []
            for lab in l[1:]:
                try:
                    # if number, get name
                    lab_idx = int(lab) + 1
                    labs.append(self.label_id2name(lab_idx))
                except ValueError:
                    # if str, use str as name
                    labs.append(lab)

            labels_dict[osp.normpath(l[0])] = labs

        data_paths = listdir(data_dir, filters)
        for data_path in data_paths:
            labels = labels_dict.get(osp.normpath(data_path), [])
            self.add_task([{"path": data_path}], [[{"label_name": name} for name in labels]])

        self.commit()

    def list_exporter(self, export_dir):
        project = self.project

        # 1. all images
        # - with annotation go to export_dir/image
        # - without annotation go to export_dir/no_annotation
        create_dir(osp.join(export_dir, "image"))
        create_dir(osp.join(export_dir, "no_annotation"))
        have_no_annotation = False

        # 2. write labels.txt
        self.export_labels(osp.join(export_dir, "labels.txt"))

        # 3. move all images to image folder
        tasks = Task._get(project_id=project.project_id, many=True)
        new_paths = []
        for task in tasks:
            for data in task.datas:
                if len(data.annotations) == 0:
                    folder = "no_annotation"
                    have_no_annotation = True
                else:
                    folder = "image"

                copy(
                    osp.join(project.data_dir, data.path),
                    osp.join(export_dir, folder, osp.basename(data.path)),
                )
                new_paths.append([osp.join(folder, osp.basename(data.path))])
        if not have_no_annotation:
            shutil.rmtree(osp.join(export_dir, "no_annotation"))

        # 4. export split
        self.export_split(osp.join(export_dir), tasks, new_paths)


class ProjectSubtypeSelector:
    __persist__: list[str] = ["clasSubCatg"]

    def __init__(self):
        self.import_questions = []
        self.export_questions = []
        self.iq = partial(self.add_q, self.import_questions)
        self.eq = partial(self.add_q, self.export_questions)

        self.iq(
            label="clasSubCatg",
            required=True,
            type="choice",
            choices=[("singleClass", None), ("multiClass", None)],
            tips=None,
            show_after=None,
        )
        self.iq(
            label="labelFormat",
            required=True,
            type="choice",
            choices=[("singleClassFolder", None), ("singleClassList", None)],
            tips=None,
            show_after=[("clasSubCatg", "singleClass")],
        )
        self.iq(
            label="labelFormat",
            required=True,
            type="choice",
            choices=[("multiClassList", None)],
            tips=None,
            show_after=[("clasSubCatg", "multiClass")],
        )

    def get_handler(self, answers: dict | None, project: Project):
        if answers is None:
            return SingleClass(project=project, is_export=False)
        clas_sub_catg = answers["clasSubCatg"]
        if clas_sub_catg == "singleClass":
            return SingleClass(project=project, is_export=False)
        return MultiClass(project=project, is_export=False)

    def get_importer(self, answers: dict | None, project: Project):
        handler = self.get_handler(answers, project)
        if answers is None:
            return handler.importers["singleClassFolder"]
        label_format = answers["labelFormat"]
        if label_format == "noLabel":
            return handler.default_importer
        return handler.importers[label_format]

    @validate_arguments
    def add_q(
        self,
        question_set: list,
        label: str,  # can have duplicates. Maybe same question, different choices
        required: bool,
        type: str,  # "choice", "input"
        choices: list[tuple[str, str | None]] | None,
        tips: str | None,
        show_after: list[tuple[str, str]] | None,
        is_arg: bool = False,
    ):
        question_set.append(
            {
                "label": label,
                "required": required,
                "type": type,
                "choices": choices,
                "tips": tips,
                "show_after": [] if show_after is None else show_after,
            }
        )
