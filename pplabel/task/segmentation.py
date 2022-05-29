import os.path as osp


import numpy as np
import cv2

from pplabel.task.util import create_dir, listdir, image_extensions
from pplabel.task.base import BaseTask
from pplabel.config import db
from pplabel.task.util.color import hex_to_rgb
from pplabel.task.util import copy
from pplabel.api.model import Task, Annotation

# debug
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("TkAgg")


def parse_semantic_mask(annotation_path, labels):
    ann = cv2.imread(annotation_path, cv2.IMREAD_UNCHANGED)
    frontend_id = 1
    anns = []
    # TODO: len(ann.shape == 3) and ann.shape[-1] == 1 necessary?
    if len(ann.shape) == 2 or (len(ann.shape) == 3 and ann.shape[-1] == 1):
        for label in labels:
            # plt.imshow(ann)
            # plt.show()
            x, y = np.where(ann == label.id)
            result = ",".join([f"{y},{x}" for x, y in zip(x, y)])
            result = f"{0},{frontend_id}," + result
            anns.append({"label_name": label.name, "result": result, "type": "brush"})
            frontend_id += 1
    else:
        ann = cv2.cvtColor(ann, cv2.COLOR_BGR2RGB)
        for label in labels:
            color = hex_to_rgb(label.color)
            label_mask = np.all(ann == color, axis=2).astype("uint8")
            x, y = np.where(label_mask == 1)
            result = ",".join([f"{y},{x}" for x, y in zip(x, y)])
            result = f"{0},{frontend_id}," + result
            anns.append({"label_name": label.name, "result": result, "type": "brush"})
            frontend_id += 1
    s = [1] + list(ann.shape)
    s = [str(s) for s in s]
    size = ",".join(s)
    return size, anns

    # ccnum, markers = cv2.connectedComponents(label_mask)
    # for ccidx in range(1, ccnum + 1):


class SemanticSegmentation(BaseTask):
    def __init__(self, project):
        super().__init__(project, skip_label_import=True)
        self.importers = {
            "mask": self.mask_importer,
            "polygon": self.default_importer,
        }
        self.exporters = {
            "mask": self.mask_exporter,
            "polygon": self.mask_exporter,
        }

    def mask_importer(
        self,
        data_dir=None,
        filters={"exclude_prefix": ["."], "include_postfix": image_extensions},
    ):
        # 1. set params
        project = self.project
        if data_dir is None:
            base_dir = project.data_dir
            data_dir = osp.join(base_dir, "JPEGImages")
            ann_dir = osp.join(base_dir, "Annotations")
        # TODO: save background name
        self.import_labels(ignore_first=True)

        ann_dict = {osp.basename(p).split(".")[0]: p for p in listdir(ann_dir, filters)}

        # 2. import records
        for data_path in listdir(data_dir, filters):
            id = osp.basename(data_path).split(".")[0]
            data_path = osp.join(data_dir, data_path)
            if id in ann_dict.keys():
                ann_path = osp.join(ann_dir, ann_dict[id])
                size, anns = parse_semantic_mask(ann_path, project.labels)
            else:
                anns = None

            self.add_task([{"path": data_path, "size": size}], [anns])
        db.session.commit()

        # # 3. move data
        # if data_dir != project.data_dir:
        #     copytree(data_dir, project.data_dir)

    def mask_exporter(self, export_dir, type="grayscale"):
        # 1. set params
        project = self.project

        export_data_dir = osp.join(export_dir, "JPEGImages")
        export_label_dir = osp.join(export_dir, "Annotations")
        create_dir(export_data_dir)
        create_dir(export_label_dir)

        tasks = Task._get(project_id=project.project_id, many=True)
        export_data_paths = []
        export_label_paths = []

        for task in tasks:
            data = task.datas[0]
            data_path = osp.join(project.data_dir, data.path)
            export_data_path = osp.join("JPEGImages", osp.basename(data.path))
            # TODO: strip ext
            export_label_path = osp.join(
                export_label_dir, osp.basename(data_path).split(".")[0] + ".png"
            )

            copy(data_path, export_data_dir)
            width, height = map(int, data.size.split(",")[1:3])
            if type == "pesudo":
                mask = np.zeros((width, height, 3))
                for ann in task.annotations:
                    color = hex_to_rgb(ann.label.color)[::-1]
                    points = ann.result.split(",")[2:]
                    points = [int(p) for p in points]
                    for idx in range(0, len(points), 2):
                        y = points[idx]
                        x = points[idx + 1]
                        mask[x, y, :] = color
            elif type == "grayscale":
                mask = np.zeros((width, height))
                for ann in task.annotations:
                    label_id = ann.label.label_id
                    points = ann.result.split(",")[2:]
                    points = [int(p) for p in points]
                    for idx in range(0, len(points), 2):
                        y = points[idx]
                        x = points[idx + 1]
                        mask[x, y] = label_id
            cv2.imwrite(export_label_path, mask)


            export_data_paths.append([export_data_path])
            export_label_paths.append([export_label_path])

        self.export_split(export_dir, tasks, export_data_paths, with_labels=False)
        self.export_labels(osp.join(export_dir, "labels.txt"))

    def pesudo_color_exporter(self, export_dir):
        pass


"""
/home/lin/Desktop/git/label/data/export/
"""
