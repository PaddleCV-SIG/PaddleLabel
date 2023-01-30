# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
import shutil

from paddlelabel.task.util.labelme import LabelMe
from paddlelabel.api import Task
from paddlelabel.task.util import create_dir, copy, image_extensions
from paddlelabel.task.base import BaseTask
from paddlelabel.io.image import getSize


class Point(BaseTask):
    def __init__(self, project, data_dir: Path, is_export=False):
        super(Point, self).__init__(project, data_dir=data_dir, skip_label_import=True, is_export=is_export)
        self.importers = {
            "labelme": self.labelme_importer,
        }
        self.exporters = {
            "labelme": self.labelme_exporter,
        }

    def labelme_importer(
        self,
        data_dir: Path,
        filters={"exclude_prefix": ["."], "include_postfix": image_extensions},
    ):
        data_dir = Path(data_dir)
        # 1. set params
        self.create_warning(data_dir)

        # 2. import all datas
        labelme = LabelMe(data_dir)
        for img_path, (ann_path, set_idx) in labelme.matchings.items():
            # print(ann_path)
            if ann_path is not None:
                height, width, anns = labelme.parse_ann(ann_path, set(["point"]))
                size = f"1,{height},{width}"
            else:
                size, _, _ = getSize(img_path)
                anns = []
            # print(anns)
            self.add_task([{"path": str(img_path), "size": size}], [anns], set_idx)

        self.commit()

    def labelme_exporter(self, export_dir):
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
