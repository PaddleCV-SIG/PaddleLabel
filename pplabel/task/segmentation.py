import os.path as osp

import numpy as np
import cv2

from pplabel.task.util import create_dir, listdir, image_extensions
from pplabel.task.base import BaseTask
from pplabel.config import db
from pplabel.task.util.color import hex_to_rgb

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
            plt.imshow(ann)
            plt.show()
            x, y = np.where(ann == label.id)
            result = ",".join([f"{y},{x}" for x, y in zip(x, y)])
            result = f"{0},{frontend_id}," + result
            anns.append({"label_name": label.name, "result": result, "type":"brush"})
            frontend_id += 1
    else:
        ann = cv2.cvtColor(ann, cv2.COLOR_BGR2RGB)
        for label in labels:
            color = hex_to_rgb(label.color)
            label_mask = np.all(ann == color, axis=2).astype("uint8")
            x, y = np.where(label_mask == 1)
            result = ",".join([f"{y},{x}" for x, y in zip(x, y)])
            result = f"{0},{frontend_id}," + result
            anns.append({"label_name": label.name, "result": result, "type":"brush"})
            frontend_id += 1

    return anns

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
            "mask": self.gray_scale_exporter,
            "polygon": self.pesudo_color_exporter,
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
                print(data_path, ann_path)
                anns = parse_semantic_mask(ann_path, project.labels)
            else:
                anns = None

            self.add_task([{"path": data_path}], [anns])
        db.session.commit()

        # # 3. move data
        # if data_dir != project.data_dir:
        #     copytree(data_dir, project.data_dir)


    def gray_scale_exporter(self, export_dir):
        pass

    def pesudo_color_exporter(self, export_dir):
        pass
