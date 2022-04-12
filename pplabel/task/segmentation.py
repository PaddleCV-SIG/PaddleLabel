import os.path as osp

from pplabel.config import db, task_test_basedir
from pplabel.api import Project, Task, Data, Annotation, Label
from pplabel.api.schema import ProjectSchema
from .util import create_dir, listdir, copy, copytree, image_extensions
from .base import BaseTask


class SemanticSegmentation(BaseTask):
    def __init__(self, project):
        super().__init__(project)
        self.importers = {
            "gray_scale": self.gray_scale_importer,
        }
        self.exporters = {
            "gray_scale": self.single_class_exporter,
        }

    def gray_scale_importer(
        self,
        data_dir=None,
        label_dir=None,
        filters={"exclude_prefix": ["."], "include_postfix": image_extensions},
    ):
        project = self.project
        if data_dir is None:
            data_dir = project.data_dir
        if label_path is None:
            label_path = project.label_dir

        # 1. if data_dir/labels.txt exists, import labels
        # TODO: last string as color
        if label_path is not None and osp.exists(label_path):
            labels = open(label_path, "r").readlines()
            labels = [l.strip() for l in labels if len(l.strip()) != 0]
            for lab in labels:
                self.add_label(lab)

        # 2. import records
        create_dir(data_dir)
        for data_path in listdir(data_dir, filters):
            if data_path == label_path:
                continue
            if project.data_dir in data_path:
                data_path = osp.relpath(data_path, project.data_dir)
            label_name = osp.basename(osp.dirname(data_path))
            self.add_task([data_path], [[{"label_name": label_name}]])
            print(f"==== {data_path} imported ====")

        # 3. move data
        if data_dir != project.data_dir:
            copytree(data_dir, project.data_dir)

    def gray_scale_exporter(self, export_dir):
        create_dir(export_dir)

        project = self.project
        labels = Label._get(project_id=project.project_id, many=True)
        labels.sort(key=lambda l: l.id)
        label_idx = {}
        for idx, label in enumerate(labels):
            label_idx[label.name] = idx
        with open(osp.join(export_dir, "labels.txt"), "w") as f:
            for lab in labels:
                print(lab.name, file=f)

        for label in labels:
            dir = osp.join(export_dir, label.name)
            create_dir(dir)

        set_names = ["train", "validation", "test"]
        set_files = [open(osp.join(export_dir, f"{n}.txt"), "w") for n in set_names]
        tasks = Task._get(project_id=project.project_id, many=True)
        for task in tasks:
            for data in task.datas:
                label_name = ""
                if len(data.annotations) == 1:
                    label_name = data.annotations[0].label.name
                    print(
                        f"{osp.join(label_name, osp.basename(data.path))} {label_idx[label_name]}",
                        file=set_files[task.set],
                    )
                dst = osp.join(export_dir, label_name)
                copy(osp.join(project.data_dir, data.path), dst)

        for f in set_files:
            f.close()

            print(
                f"JPEGImages/{osp.basename(data_path)} Annotations/{id}.xml",
                file=set_files[task.set],
            )
        for f in set_files:
            f.close()

    
def voc():
    pj_info = {
        "name": "Pascal Segmentation Example",
        "data_dir": osp.join(task_test_basedir, "seg_pascal_voc/JPEGImages/"),
        "task_category_id": 3,
        "label_dir": osp.join(task_test_basedir, "seg_pascal_voc/Annotations/"),
    }
    project = ProjectSchema().load(pj_info)

    seg_project = Segmentation(project)

    seg_project.voc_importer(filters={"exclude_prefix": ["."]})

    seg_project.voc_exporter(osp.join(task_test_basedir, "export/seg_voc_export"))


def coco():
    pj_info = {
        "name": "COCO Segmentation Example",
        "data_dir": osp.join(task_test_basedir, "seg_coco/JPEGImages/"),
        "description": "Example Project Descreption",
        "label_dir": osp.join(task_test_basedir, "seg_coco/Annotations/coco_info.json"),
        "task_category_id": 3,
    }
    project = ProjectSchema().load(pj_info)

    seg_project = Segmentation(project)

    seg_project.coco_importer(filters={"exclude_prefix": ["."]})

    seg_project.coco_exporter(osp.join(task_test_basedir, "export/seg_coco_export"))
