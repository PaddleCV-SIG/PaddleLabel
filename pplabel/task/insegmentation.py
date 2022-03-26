import os
import os.path as osp
import json

from pycocotools.coco import COCO

from pplabel.config import db, task_test_basedir
from pplabel.api import Project, Task, Data, Annotation, Label
from pplabel.api.schema import ProjectSchema
from .util import create_dir, listdir, copy, copytree, ComponentManager
from .base import BaseTask


# FIXME: update inssegmentation parse_voc_label and create_voc_label
def parse_voc_label(label_path):
    pass


def create_voc_label(filename, width, height, annotations):
    pass


class InsSegmentation(BaseTask):
    importers = ComponentManager()
    exporters = ComponentManager()

    @importers.add_component
    def coco_importer(
        self,
        data_dir=None,
        label_path=None,
        filters={"exclude_prefix": ["."]},
    ):
        project = self.project
        if data_dir is None:
            data_dir = project.data_dir
        success, res = create_dir(data_dir)
        if not success:
            return False, res
        if label_path is None:
            label_path = project.label_dir

        coco = COCO(label_path)

        ann_by_task = {}
        for ann_id in coco.getAnnIds():
            ann = coco.anns[ann_id]
            label_name = coco.cats[ann["category_id"]]["name"]
            result = {}
            result["xmin"] = ann["bbox"][0]
            result["ymin"] = ann["bbox"][1]
            result["xmax"] = result["xmin"] + ann["bbox"][2]
            result["ymax"] = result["ymin"] + ann["bbox"][3]
            temp = ann_by_task.get(ann["image_id"], [])
            temp.append({"label_name": label_name, "result": json.dumps(result)})
            ann_by_task[ann["image_id"]] = temp
        for img_id, annotations in list(ann_by_task.items()):
            self.add_task([coco.imgs[img_id]["file_name"]], annotations)

    @importers.add_component
    def voc_importer(
        self,
        data_dir=None,
        label_dir=None,
        filters={"exclude_prefix": ["."]},
    ):
        project = self.project
        if data_dir is None:
            data_dir = project.data_dir
        if label_dir is None:
            label_dir = project.label_dir
        success, res = create_dir(data_dir)
        if not success:
            return False, res
        if label_dir is not None:
            success, res = create_dir(data_dir)
            if not success:
                return False, res
        data_paths = listdir(data_dir)
        label_paths = listdir(label_dir)
        label_dict = {}
        for label_path in label_paths:
            label_dict[osp.basename(label_path).split(".")[0]] = label_path
        for data_path in data_paths:
            id = osp.basename(data_path).split(".")[0]
            self.add_task([data_path], parse_voc_label(label_dict[id]))

    @exporters.add_component
    def coco_exporter(self, export_dir):
        project = self.project
        coco = COCO()
        labels = Label._get(project_id=project.project_id, many=True)
        for label in labels:
            coco.addCategory(label.id, label.name, label.color)
        tasks = Task._get(project_id=project.project_id, many=True)
        data_dir = osp.join(export_dir, "JPEGImages")
        create_dir(data_dir)
        for task in tasks:
            coco.addImage(task.datas[0].path, 1000, 1000, task.task_id)
            copy(osp.join(project.data_dir, task.datas[0].path), data_dir)
        annotations = Annotation._get(project_id=project.project_id, many=True)
        for ann in annotations:
            r = json.loads(ann.result)
            bb = [r["xmin"], r["ymin"], r["xmax"] - r["xmin"], r["ymax"] - r["ymin"]]
            coco.addAnnotation(
                ann.task.datas[0].path, ann.label_id, [], id=ann.annotation_id, bbox=bb
            )
        create_dir(osp.join(export_dir, "Annotations"))
        f = open(osp.join(export_dir, "Annotations", "coco_info.json"), "w")
        print(json.dumps(coco.dataset), file=f)
        f.close()

    @exporters.add_component
    def voc_exporter(self, export_dir):
        project = self.project
        tasks = Task._get(project_id=project.project_id, many=True)
        export_data_dir = osp.join(export_dir, "JPEGImages")
        export_label_dir = osp.join(export_dir, "Annotations")
        create_dir(export_data_dir)
        create_dir(export_label_dir)

        for task in tasks:
            data_path = osp.join(project.data_dir, task.datas[0].path)
            copy(data_path, export_data_dir)
            id = osp.basename(data_path).split(".")[0]
            f = open(osp.join(export_label_dir, f"{id}.xml"), "w")
            print(
                create_voc_label(osp.basename(data_path), 1000, 1000, task.annotations),
                file=f,
            )
            f.close()


def voc():
    pj_info = {
        "name": "Pascal InsSegmentation Example",
        "data_dir": osp.join(task_test_basedir, "inseg_pascal_voc/JPEGImages/"),
        "task_category_id": 3,
        "label_dir": osp.join(task_test_basedir, "inseg_pascal_voc/Annotations/"),
    }
    project = ProjectSchema().load(pj_info)

    seg_project = InsSegmentation(project)

    seg_project.voc_importer(filters={"exclude_prefix": ["."]})

    seg_project.voc_exporter(
        osp.join(task_test_basedir, "export/inseg_voc_export")
    )


def coco():
    pj_info = {
        "name": "COCO InsSegmentation Example",
        "data_dir": osp.join(task_test_basedir, "inseg_coco/JPEGImages/"),
        "description": "Example Project Descreption",
        "label_dir": osp.join(task_test_basedir, "inseg_coco/Annotations/coco_info.json"),
        "task_category_id": 3,
    }
    project = ProjectSchema().load(pj_info)

    seg_project = InsSegmentation(project)

    seg_project.coco_importer(filters={"exclude_prefix": ["."]})

    seg_project.coco_exporter(
        osp.join(task_test_basedir, "export/inseg_coco_export")
    )
