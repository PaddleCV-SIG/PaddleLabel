import os.path as osp
import json

from pycocotoolse.coco import COCO

from pplabel.api import Task, Annotation, Label
from pplabel.task.util import create_dir, listdir, copy, image_extensions
from pplabel.task.base import BaseTask
from pplabel.config import db

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
    r = json.loads(ann.result)
    for ann in annotations:
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
    # TODO: beautify export xml
    # return minidom.parseString(voc_label.strip()).toprettyxml(indent="    ", newl="")
    return voc_label.strip()


class Detection(BaseTask):
    def __init__(self, project):
        super().__init__(project)
        self.importers = {"coco": self.coco_importer, "voc": self.voc_importer}
        self.exporters = {"coco": self.coco_exporter, "voc": self.voc_exporter}  # TODO: change
        # self.default_importer = self.default_importer # default to voc
        self.default_importer = self.voc_exporter  # default to voc
        self.default_exporter = self.voc_importer

    def coco_importer(
        self,
        data_dir=None,
        filters={"exclude_prefix": ["."], "include_postfix": image_extensions},
    ):
        """
        images should be located at data_dir / file_name in coco annotation
        """

        # 1. set params
        project = self.project
        if data_dir is None:
            data_dir = project.data_dir
        # TODO: coco train val test json
        label_file_paths = ["train.json", "val.json", "test.json"]
        label_file_paths = [osp.join(data_dir, f) for f in label_file_paths]

        def _coco_importer(data_paths, label_file_path, set=0):
            coco = COCO(label_file_path)
            # get image full paths
            for idx, img in coco.imgs.items():
                # print(idx, img)
                file_name = img["file_name"]
                full_path = filter(lambda p: p[-len(file_name) :] == file_name, data_paths)
                full_path = list(full_path)
                if len(full_path) != 1:
                    raise RuntimeError(
                        f"{'No' if len(full_path) == 0 else 'Multiple'} image(s) with path ending with {file_name} found under {data_dir}"
                    )
                full_path = full_path[0]
                data_paths.remove(full_path)
                coco.imgs[idx]["full_path"] = full_path
                # print("----", file_name, full_path)

            # get ann by image
            ann_by_task = {}
            for ann_id in coco.getAnnIds():
                ann = coco.anns[ann_id]
                label_name = coco.cats[ann["category_id"]]["name"]
                # result = {}
                # result["xmin"] = ann["bbox"][0]
                # result["ymin"] = ann["bbox"][1]
                # result["xmax"] = result["xmin"] + ann["bbox"][2]
                # result["ymax"] = result["ymin"] + ann["bbox"][3]
                # image center as origin, right x down y
                res = ann["bbox"]
                width, height = (
                    coco.imgs[ann["image_id"]].get("width", None),
                    coco.imgs[ann["image_id"]].get("height", None),
                )
                res[2] += res[0]
                res[3] += res[1]
                res[0] -= width / 2
                res[1] -= height / 2
                res[2] -= width / 2
                res[3] -= height / 2

                res = [str(r) for r in res]
                res = ",".join(res)
                curr_anns = ann_by_task.get(ann["image_id"], [])
                curr_anns.append(
                    {
                        "label_name": label_name,
                        "result": res,
                        "type": "rectangle",
                        "frontend_id": len(curr_anns) + 1,
                    }
                )
                ann_by_task[ann["image_id"]] = curr_anns

            # add tasks
            for img_id, annotations in list(ann_by_task.items()):
                data_path = coco.imgs[img_id]["full_path"]
                # print("annotations", annotations)
                self.add_task([data_path], [annotations], split=set)
            return data_paths

        data_paths = listdir(data_dir, filters=filters)
        for split_idx, label_file_path in enumerate(label_file_paths):
            data_paths = _coco_importer(data_paths, label_file_path, split_idx)

        # add tasks without label
        for data_path in data_paths:
            self.add_task([data_path])

        db.session.commit()

    def voc_importer(
        self,
        data_dir=None,
        filters={"exclude_prefix": ["."]},
    ):
        project = self.project
        base_dir = data_dir
        if base_dir is None:
            base_dir = project.data_dir

        data_dir = osp.join(base_dir, "JPEGImages")
        label_dir = osp.join(base_dir, "Annotations")

        create_dir(data_dir)

        data_paths = listdir(data_dir, filters=filters)
        label_paths = listdir(label_dir, filters=filters)
        data_paths = [osp.join(data_dir, p) for p in data_paths]
        label_paths = [osp.join(label_dir, p) for p in label_paths]

        label_name_dict = {}
        labels = []
        for label_path in label_paths:
            labels.append(parse_voc_label(label_path))
            label_name_dict[osp.basename(label_path).split(".")[0]] = len(labels) - 1

        for data_path in data_paths:
            id = osp.basename(data_path).split(".")[0]
            label_idx = label_name_dict.get(id, -1)
            self.add_task([data_path], [labels[label_idx] if label_idx != -1 else []])
        db.session.commit()

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

    def voc_exporter(self, export_dir):
        project = self.project
        tasks = Task._get(project_id=project.project_id, many=True)
        export_data_dir = osp.join(export_dir, "JPEGImages")
        export_label_dir = osp.join(export_dir, "Annotations")
        create_dir(export_data_dir)
        create_dir(export_label_dir)

        set_names = ["train.txt", "validation.txt", "test.txt"]
        set_files = [open(osp.join(export_dir, n), "w") for n in set_names]
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

            print(
                f"JPEGImages/{osp.basename(data_path)} Annotations/{id}.xml",
                file=set_files[task.set],
            )
        for f in set_files:
            f.close()
