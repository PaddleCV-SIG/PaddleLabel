# -*- coding: utf-8 -*-
from __future__ import annotations
import os.path as osp
import json

from copy import deepcopy
from PIL import Image
from pathlib import Path
import numpy as np
import cv2

from paddlelabel.io.image import getSize
from paddlelabel.task.instance_segmentation import InstanceSegmentation, draw_mask
from paddlelabel.task.util import create_dir, listdir, image_extensions, copy
from paddlelabel.task.util.color import hex_to_rgb
from paddlelabel.api.model import Task


def parse_semantic_mask(annotation_path, labels, image_path=None):
    ann_img = Image.open(annotation_path)
    ann = np.array(ann_img.convert(mode=ann_img.mode))  # size is hwc

    if image_path is not None:
        img = Image.open(annotation_path)
        if img.size[::-1] != ann.shape[:2]:
            raise RuntimeError(
                f"Image ({img.size[::-1]}) and annotation ({ann.shape[:2]}) has different shapes, please check image {image_path} and annotation {annotation_path}",
            )
    frontend_id = 1
    anns = []
    if len(ann.shape) == 3:
        # ann = cv2.cvtColor(ann, cv2.COLOR_BGR2RGB)
        ann_gray = np.zeros(ann.shape[:2], dtype="uint8")
        for label in labels:
            color = hex_to_rgb(label.color)
            label_mask = np.all(ann == color, axis=2)
            ann_gray[label_mask == 1] = label.id
            ann[label_mask == 1] = 0
        if ann.sum() != 0:
            ann = ann.reshape((-1, ann.shape[-1]))
            raise RuntimeError(
                f"Pseudo color mask {annotation_path} contains color that's not specified in labels {np.unique(ann, axis=0)[1:].tolist()} . Maybe you didn't include a background class in the first line of labels.txt or didn't specify label color?"
            )
        ann = ann_gray

    for label in labels:
        label_mask = deepcopy(ann)
        label_mask[label_mask != label.id] = 0
        label_mask[label_mask != 0] = 255

        if label_mask.sum() == 0:
            continue

        ann[ann == label.id] = 0
        (cc_num, cc_mask, values, centroid) = cv2.connectedComponentsWithStats(label_mask, connectivity=8)
        for cc_id in range(1, cc_num):
            h, w = np.where(cc_mask == cc_id)
            result = ",".join([f"{w},{h}" for h, w in zip(h, w)])
            # result = f"{1},{frontend_id}," + result
            # TODO: patch. points type will be set by ann.type
            result = f"{0},{0}," + result
            anns.append(
                {
                    "label_name": label.name,
                    "result": result,
                    "type": "brush",
                    "frontend_id": label.id,
                }
            )
            frontend_id += 1

    if ann.sum() != 0:
        msg = f"Mask {annotation_path} contains unspecified labels {np.unique(ann)[1:].tolist()} . Maybe you didn't include a background class in the first line of labels.txt or didn't specify label id?"
        abort(msg, 404)

    s = (1,) + tuple(ann.shape[:2])
    s = [str(s) for s in s]
    size = ",".join(s)
    return size, anns


class SemanticSegmentation(InstanceSegmentation):
    def __init__(self, project, data_dir=None, is_export=False):
        super().__init__(project, data_dir=data_dir, is_export=is_export)
        self.importers = {
            "mask": self.mask_importer,
            "coco": self.coco_importer,
            "eiseg": self.eiseg_importer,
        }
        self.exporters = {
            "mask": self.mask_exporter,
            "coco": self.coco_exporter,
        }
        self.default_exporter = self.mask_exporter

    def mask_importer(
        self,
        data_dir=None,
        filters={"exclude_prefix": ["."], "include_postfix": image_extensions},
    ):

        # 1. set params
        project = self.project

        base_dir = project.data_dir if data_dir is None else data_dir

        data_dir = osp.join(base_dir, "JPEGImages")
        ann_dirs = [
            Path(base_dir) / "Annotations",
            Path(base_dir) / "label",  # EISeg
        ]

        background_line = self.import_labels(ignore_first=True)
        other_settings = project._get_other_settings()
        other_settings["background_line"] = background_line
        project.other_settings = json.dumps(other_settings)

        ann_dict = {}
        for ann_dir in ann_dirs:
            paths = listdir(ann_dir, filters)
            ann_dict.update({osp.basename(p).split(".")[0]: ann_dir / p for p in paths})
            if ann_dir.name == "label":
                ann_dict.update(
                    {
                        osp.basename(p).split(".")[0][: -len("_pseudo")]: ann_dir / p
                        for p in paths
                        if "_pseudo" in Path(p).name
                    }
                )  # NOTE: EISeg pseudo color label export

        # 2. import records
        data_paths = listdir(data_dir, filters)
        if len(data_paths) == 0:
            raise RuntimeError("No image found. Did you put images under JPEGImages folder?")

        for data_path in data_paths:
            id = osp.basename(data_path).split(".")[0]
            data_path = osp.join(data_dir, data_path)
            if id in ann_dict.keys():
                ann_path = osp.join(ann_dir, ann_dict[id])
                size, anns = parse_semantic_mask(ann_path, project.labels, data_path)
            else:
                anns = []
                size, _, _ = getSize(Path(data_path))

            self.add_task([{"path": data_path, "size": size}], [anns])
        self.commit()

    def mask_exporter(self, export_dir: str, seg_mask_type: str = "grayscale"):
        """Export semantic segmentation dataset in mask format

        Args:
            export_dir (str): The folder to export to.
            seg_mask_type (str): grayscale|pseudo
        """

        # 1. set params
        project = self.project
        # other_settings = project._get_other_settings()
        # mask_type = other_settings.get("segMaskType", "grayscale")

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
            export_label_path = osp.join(export_label_dir, osp.basename(data_path).split(".")[0] + ".png")

            copy(data_path, export_data_dir)

            mask = draw_mask(data, mask_type=seg_mask_type)
            mask_img = Image.fromarray(mask.astype("uint8"), "L")
            mask_img.save(export_label_path)

            export_data_paths.append([export_data_path])
            export_label_paths.append([export_label_path])

        self.export_split(
            Path(export_dir),
            tasks,
            export_data_paths,
            with_labels=False,
            annotation_ext=".png",
        )
        bg = project._get_other_settings().get("background_line", "background")
        self.export_labels(osp.join(export_dir, "labels.txt"), bg)
