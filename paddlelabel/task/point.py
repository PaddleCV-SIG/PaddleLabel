# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
import shutil

from paddlelabel.task.util.labelme import get_matching, parse_ann, write_ann
from paddlelabel.api import Task, Project
from paddlelabel.task.base import BaseSubtypeSelector, BaseTask
from paddlelabel.io.image import getSize


class Point(BaseTask):
    def __init__(self, project, data_dir: Path | None = None, is_export=False):
        super(Point, self).__init__(project, data_dir=data_dir, skip_label_import=True, is_export=is_export)
        self.importers = {
            "labelme": self.labelme_importer,
        }
        self.exporters = {
            "labelme": self.labelme_exporter,
        }

    def labelme_importer(self, data_dir: Path):
        # 1. set params
        data_dir = Path(data_dir)
        self.create_warning(data_dir)

        # 2. import all datas
        for img_path, (ann_path, set_idx) in get_matching(data_dir).items():
            if ann_path is not None:
                height, width, anns = parse_ann(ann_path, set(["point"]))
                size = f"1,{height},{width}"
            else:
                anns = []
                size, _, _ = getSize(img_path)
            self.add_task([{"path": str(img_path), "size": size}], [anns], set_idx)

        self.commit()

    def labelme_exporter(self, export_dir: Path):
        # 1. set params, prep output folders
        project = self.project

        export_dir = Path(export_dir)
        export_dir.mkdir(exist_ok=True, parents=True)
        img_dst = export_dir / "JPEGImages"
        ann_dst = export_dir / "Annotations"
        img_dst.mkdir()
        ann_dst.mkdir()
        data_dir = Path(project.data_dir)

        # 2. move images and write ann json
        tasks = Task._get(project_id=project.project_id, many=True)
        new_paths = []
        for task in tasks:
            data = task.datas[0]
            _, height, width = map(int, data.size.split(","))
            img_path = img_dst / Path(data.path).name
            ann_path = ann_dst / (Path(data.path).name.split(".")[0] + ".json")
            shutil.copy(data_dir / data.path, img_path)
            write_ann(ann_path, img_path, height, width, data.annotations, with_data=False)

            new_paths.append([str(img_path.relative_to(export_dir))])
        print(new_paths)

        # 3. write split files
        self.export_split(export_dir, tasks, new_paths, with_labels=False, annotation_ext=".json")


class ProjectSubtypeSelector(BaseSubtypeSelector):
    def __init__(self):
        super(ProjectSubtypeSelector, self).__init__()

        self.iq(
            label="labelFormat",
            required=True,
            type="choice",
            choices=[("labelme", None)],
            tips=None,
            show_after=None,
        )

    def get_handler(self, answers: dict | None, project: Project):
        return Point(project=project, is_export=False)

    def get_importer(self, answers: dict | None, project: Project):
        handler = self.get_handler(answers, project)
        if answers is None:
            return handler.importers["labelme"]
        label_format = answers["labelFormat"]
        if label_format == "noLabel":
            return handler.default_importer
        return handler.importers[label_format]
