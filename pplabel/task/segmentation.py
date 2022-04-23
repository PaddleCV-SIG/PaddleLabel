import os.path as osp
from pplabel.api.model import annotation

from pplabel.api import Project, Task, Data, Annotation, Label
from pplabel.api.schema import ProjectSchema
from pplabel.task.util import create_dir, listdir, copy, copytree, image_extensions
from .base import BaseTask

import cv2

import matplotlib.pyplot as plt


def parse_gray_annotation(annotation_path):
    print("parsing", annotation_path)
    ann = cv2.imread(annotation_path, cv2.IMREAD_GRAYSCALE)
    print(type(ann), ann.shape)
    plt.imshow(ann)
    plt.show()


class SemanticSegmentation(BaseTask):
    def __init__(self, project):
        super().__init__(project)
        self.importers = {
            "gray_scale": self.gray_scale_importer,
            "pesudo_color": self.pesudo_color_importer,
        }
        self.exporters = {
            "gray_scale": self.gray_scale_exporter,
            "pesudo_color": self.pesudo_color_exporter,
        }

    def gray_scale_importer(
        self,
        data_dir=None,
        label_file_path=None,
        filters={"exclude_prefix": ["."], "include_postfix": image_extensions},
    ):
        project = self.project
        if data_dir is None:
            data_dir = osp.join(project.data_dir, "JPEGImages")
            annotation_dir = osp.join(project.data_dir, "Annotations")
        if label_file_path is None:
            label_file_path = project.label_dir

        # 1. if data_dir/labels.txt exists, import labels
        # TODO: last string as color
        self.import_label_file(label_file_path)
        
        # 2. import records
        create_dir(data_dir)
        for data_path in listdir(data_dir, filters):
            annotation_path = data_path.replace("JPEGImages", "Annotations")
            parse_gray_annotation(annotation_path)
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
