import os
import os.path as osp
import json

from pplabel.config import db
from pplabel.api import Project, Task, Data, Annotation, Label
from pplabel.api.schema import ProjectSchema
from .util import create_dir, listdir, copy, copytree, ComponentManager
from .base import BaseTask

# TODO: move to io
def parse_voc_label(label_path):
    from xml.dom import minidom

    def data(elements):
        return elements[0].firstChild.data

    file = minidom.parse(label_path)
    objects = file.getElementsByTagName("object")
    res = []
    for object in objects:
        temp = {}
        temp["label_name"] = data(object.getElementsByTagName("name"))
        bndbox = object.getElementsByTagName("bndbox")[0]
        temp["result"] = {}
        temp["result"]["xmin"] = data(bndbox.getElementsByTagName("xmin"))
        temp["result"]["xmax"] = data(bndbox.getElementsByTagName("xmax"))
        temp["result"]["ymin"] = data(bndbox.getElementsByTagName("ymin"))
        temp["result"]["ymax"] = data(bndbox.getElementsByTagName("ymax"))
        temp["result"] = json.dumps(temp["result"])
        res.append(temp)
    return res


def create_voc_label(filename, width, height, annotations):
    from xml.dom import minidom

    object_labels = ""
    for ann in annotations:
        r = json.loads(ann.result)
        object_labels += f"""
    <object>
    <name>{ann.label.name}</name>
    <bndbox>
      <xmin>{r['xmin']}</xmin>
      <ymin>{r['ymin']}</ymin>
      <xmax>{r['xmax']}</xmax>
      <ymax>{r['ymax']}</ymax>
    </bndbox>
    </object>
"""
    voc_label = f"""
<?xml version='1.0' encoding='UTF-8'?>
<annotation>
  <filename>{filename}</filename>
  <object_num>{len(annotations)}</object_num>
  <size>
    <width>{width}</width>
    <height>{height}</height>
  </size>
{object_labels}
</annotation>
"""
    # return minidom.parseString(voc_label.strip()).toprettyxml(indent="    ", newl="")
    return voc_label.strip()


class Detection(BaseTask):
    importers = ComponentManager()
    exporters = ComponentManager()

    @importers.add_component
    def coco_importer(
        self,
        data_dir=None,
        filters={"exclude_prefix": ["."]},
    ):
        pass

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
        pass

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
        "name": "Pascal Detection Example",
        "data_dir": "/home/lin/Desktop/data/pplabel/demo/det_pascal_voc/JPEGImages/",
        "task_category_id": 2,
        "label_dir": "/home/lin/Desktop/data/pplabel/demo/det_pascal_voc/Annotations/",
    }
    project = ProjectSchema().load(pj_info)

    det_project = Detection(project)

    det_project.voc_importer(filters={"exclude_prefix": ["."]})

    det_project.voc_exporter("/home/lin/Desktop/data/pplabel/demo/export/det_voc")


def multi_clas():
    pj_info = {
        "name": "Multi Class Classification Example",
        "data_dir": "/home/lin/Desktop/data/pplabel/demo/clas_multi/PetImages/",
        "description": "Example Project Descreption",
        "label_dir": "/home/lin/Desktop/data/pplabel/demo/clas_multi/label.txt",
        "other_settings": "{'some_property':true}",
        "task_category_id": 1,
        "labels": [
            {"id": 1, "name": "Cat"},
            {"id": 2, "name": "Dog"},
            {"id": 3, "name": "Small"},
            {"id": 4, "name": "Large"},
        ],
    }
    project = ProjectSchema().load(pj_info)

    clas_project = Classification(project)

    clas_project.multi_class_importer(
        filters={"exclude_prefix": ["."], "exclude_postfix": [".db"]}
    )

    clas_project.single_clas_exporter(
        "/home/lin/Desktop/data/pplabel/demo/export/multi_clas_folder_export"
    )

    clas_project.multi_clas_exporter(
        "/home/lin/Desktop/data/pplabel/demo/export/multi_clas_file_export"
    )
    tasks = Task.query.all()
    for task in tasks:
        print("tasktasktasktasktasktasktasktask", task)
    print("------------------", dir(Classification.importers["single_class_importer"]))
