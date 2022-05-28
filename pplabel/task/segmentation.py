import os.path as osp

import cv2

from pplabel.task.util import create_dir, listdir, image_extensions
from .base import BaseTask

# debug
import matplotlib.pyplot as plt


def parse_mask(annotation_path):
    ann = cv2.imread(annotation_path)
    print(type(ann), ann.shape)
    plt.imshow(ann)
    plt.show()


class SemanticSegmentation(BaseTask):
    def __init__(self, project):
        super().__init__(project)
        self.importers = {
            "mask": self.default_importer,
            "polygon": self.default_importer,
        }
        self.exporters = {
            "mask": self.gray_scale_exporter,
            "polygon": self.pesudo_color_exporter,
        }

    def mask_importer(
        self,
        data_dir=None,
        label_file_path=None,
        filters={"exclude_prefix": ["."], "include_postfix": image_extensions},
    ):
        # 1. set params
        project = self.project
        if data_dir is None:
            base_dir = project.data_dir
            data_dir = osp.join(base_dir, "JPEGImages")
            ann_dir = osp.join(base_dir, "Annotations")

        # 2. import records
        for data_path in listdir(data_dir, filters):
            data_path = osp.join(data_dir, data_path)
            ann_path = data_path.replace("JPEGImages", "Annotations")
            if not osp.exists(ann_path):
                raise RuntimeError(f"Annotation for image {data_path} doesn't exist!")
            parse_mask(ann_path)
            input("here")

            if project.data_dir in data_path:
                data_path = osp.relpath(data_path, project.data_dir)

            label_name = osp.basename(osp.dirname(data_path))

            self.add_task([data_path], [[{"label_name": label_name}]])

        # 3. move data
        if data_dir != project.data_dir:
            copytree(data_dir, project.data_dir)

    def pesudo_color_importer(
        self,
        data_dir=None,
        label_dir=None,
        filters={"exclude_prefix": ["."], "include_postfix": image_extensions},
    ):
        pass

    def gray_scale_exporter(self, export_dir):
        pass

    def pesudo_color_exporter(self, export_dir):
        pass
