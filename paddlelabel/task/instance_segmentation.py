# -*- coding: utf-8 -*-
from __future__ import annotations
import os.path as osp
import json
from copy import deepcopy
import logging

from PIL import Image
import tifffile as tif
import numpy as np
import cv2
from pycocotoolse.coco import COCO
from pathlib import Path

from paddlelabel.io.image import getSize
from paddlelabel.task.util import create_dir, listdir, image_extensions, match_by_base_name
from paddlelabel.task.base import BaseTask
from paddlelabel.task.util.color import hex_to_rgb
from paddlelabel.task.util import copy
from paddlelabel.api.model import Task, Label, Annotation
from paddlelabel.api.util import abort
from paddlelabel.api.rpc.seg import polygon2points

log = logging.getLogger("paddlelabel")


def draw_mask(data, mask_type="grayscale"):
    """Draw a segmentation mask

    Args:
        data (data record): include data info, annotation info and label info
        mask_type (str, optional): mask type, pseudo, grayscale or instance. Defaults to "grayscale".

    Returns:
        mask:
            - grayscale: [h, w, 1]
            - pseudo: [h, w, 3] rbg
            - instance: [h, w, 2] 0: instance, 1: category
    """
    height, width = map(int, data.size.split(",")[1:3])
    instance_id = 0
    if mask_type == "pseudo":
        catg_mask = np.zeros((height, width, 3))
    elif mask_type == "grayscale":
        catg_mask = np.zeros((height, width))
    elif mask_type == "instance":
        catg_mask = np.zeros((height, width))
        instance_mask = np.zeros((height, width))
    else:
        raise RuntimeError(f"Unsupported mask type: {mask_type}")

    for ann in data.annotations:
        if ann.type not in ["brush", "polygon", "points", "rubber"]:
            continue

        label_id = ann.label.id
        result = ann.result.strip().split(",")

        # TODO: path, remove this. frontend eiseg returns result that are 0,0,
        result = [r for r in result if r != ""]
        if len(result) == 2:
            continue

        instance_id += 1

        try:
            result = [int(float(p)) for p in result]
        except:
            print(ann)
            print(result, "to float error, plz open an issue for this")

        # TODO: patch. [0,fid,...] means points. to be changed
        if result[0] == 0:
            ann.type = "points"

        # TODO: patch. [not 0, 0] means brush. to be changed
        if result[0] != 0 and result[1] == 0:
            ann.type = "rubber"

        if mask_type == "pseudo":
            color = [0, 0, 0] if ann.type == "rubber" else hex_to_rgb(ann.label.color)[::-1]
        else:
            color = 0 if ann.type == "rubber" else int(label_id)

        if ann.type in ["brush", "rubber"]:
            points = result[2:]
            line_width = result[0]
            if line_width == 0:
                # print(ann, "!!!!! point/rubber type but width 0, open an issue!")
                line_width = 1
            prev_w, prev_h = points[0:2]
            try:
                for idx in range(2, len(points), 2):
                    w, h = points[idx : idx + 2]
                    cv2.line(catg_mask, (prev_w, prev_h), (w, h), color, line_width)
                    if mask_type == "instance":
                        cv2.line(instance_mask, (prev_w, prev_h), (w, h), instance_id, line_width)
                    prev_w, prev_h = w, h
            except Exception as e:
                abort(detail=e.msg, status=500, title="cv2 error")
        else:
            if ann.type == "points":
                points = result[2:]
            elif ann.type == "polygon":
                for idx in range(0, len(result), 2):
                    result[idx] = int(result[idx] + width / 2)
                    result[idx + 1] = int(result[idx + 1] + height / 2)
                points = polygon2points(result)
                points = np.array(points).reshape((-1))

            for idx in range(0, len(points), 2):
                catg_mask[points[idx + 1]][points[idx]] = color
                if mask_type == "instance":
                    instance_mask[points[idx + 1]][points[idx]] = instance_id

    if mask_type == "instance":
        return np.stack([instance_mask, catg_mask], axis=0)
    return catg_mask


def parse_instance_mask(annotation_path, labels, image_path=None):
    mask = tif.imread(annotation_path)
    if image_path is not None:
        # img = cv2.imread(annotation_path, cv2.IMREAD_UNCHANGED)
        # if img is None:
        #     raise RuntimeError(f"Read image {annotation_path} failed.")
        img = Image.open(image_path)
        # TODO: remove two paths' common prefix
        if img.size[::-1] != mask.shape[1:]:
            abort(
                f"Image {img.size[::-1]} and annotation {mask.shape[1:]} has different shape, please check image {image_path} and annotation {annotation_path}",
                500,
            )

    instance_mask = mask[0]
    label_mask = mask[1]
    anns = []

    for label in labels:
        instance_part = instance_mask[label_mask == label.id]
        instance_ids = np.unique(instance_part)
        for instance_id in instance_ids:
            h, w = np.where(instance_mask == instance_id)
            result = ",".join([f"{w},{h}" for w, h in zip(w, h)])
            # result = f"{1},{instance_id}," + result
            result = f"{0},{instance_id}," + result
            anns.append(
                {
                    "label_name": label.name,
                    "result": result,
                    "type": "brush",
                    "frontend_id": str(instance_id),
                }
            )
    s = (1,) + tuple(instance_mask.shape[:2])
    s = [str(s) for s in s]
    size = ",".join(s)
    return size, anns


class InstanceSegmentation(BaseTask):
    def __init__(self, project, data_dir=None, is_export=False):
        super().__init__(project, skip_label_import=True, data_dir=data_dir, is_export=is_export)
        self.importers = {
            "mask": self.mask_importer,
            "coco": self.coco_importer,
            "eiseg": self.eiseg_importer,
        }
        self.exporters = {
            "mask": self.mask_exporter,
            "coco": self.coco_exporter,
        }
        self.default_exporter = self.coco_exporter  # TODO: remove, user must choose

    def mask_importer(
        self,
        data_dir=None,
        filters={"exclude_prefix": ["."], "include_postfix": image_extensions},
    ):
        # 1. set params
        project = self.project

        data_dir = project.data_dir if data_dir is None else data_dir

        background_line = self.import_labels(ignore_first=True)
        other_settings = project._get_other_settings()
        other_settings["background_line"] = background_line
        project.other_settings = json.dumps(other_settings)

        ann_dict = {
            osp.basename(p).split(".")[0]: p
            for p in listdir(data_dir, {"exclude_prefix": ["."], "include_postfix": [".tiff", ".tif"]})
        }

        # 2. import records
        for data_path in listdir(data_dir, filters):
            id = osp.basename(data_path).split(".")[0]
            data_path = osp.join(data_dir, data_path)
            if id in ann_dict.keys():
                ann_path = osp.join(data_dir, ann_dict[id])
                size, anns = parse_instance_mask(ann_path, project.labels, data_path)
            else:
                anns = []
                size, _, _ = getSize(data_path)
                # mask = tif.imread(data_path)

            self.add_task([{"path": data_path, "size": size}], [anns])
        self.commit()

    def mask_exporter(self, export_dir):
        # 1. set params
        project = self.project

        # 2. create export destinations
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
            export_label_path = osp.join(export_label_dir, osp.basename(data_path).split(".")[0] + ".tiff")

            copy(data_path, export_data_dir)
            # height, width = map(int, data.size.split(",")[1:3])

            mask = draw_mask(data, mask_type="instance")
            try:
                # low version tifffile doen't have compression setting
                tif.imwrite(export_label_path, mask, compression="zlib")
            except TypeError:
                tif.imwrite(export_label_path, mask)

            export_data_paths.append([export_data_path])
            export_label_paths.append([export_label_path])

        self.export_split(
            export_dir,
            tasks,
            export_data_paths,
            with_labels=False,
            annotation_ext=".tiff",
        )
        background_line = project._get_other_settings().get("background_line")
        if not 0 in [l.id for l in project.labels] and (background_line is None or len(background_line) == 0):
            background_line = "background"

        self.export_labels(osp.join(export_dir, "labels.txt"), background_line, with_id=True)

    def coco_importer(
        self,
        data_dir: Path | None = None,
        filters: dict[str, list] = {"exclude_prefix": ["."], "include_postfix": image_extensions},
    ):
        # 1. set params
        project = self.project
        data_dir = Path(project.data_dir if data_dir is None else data_dir)
        self.split = [set()] * 3  # disable xx_list.txt support
        self.create_warning(data_dir)

        label_file_paths = [
            (["train.json"], 0),
            (["val.json"], 1),
            (["test.json"], 2),
            (["Annotations", "coco_info.json"], 0),  # EasyData format
            (["annotations.json"], 0),  # LabelMe format
            (["label", "annotations.json"], 0),  # EISeg format
        ]
        label_file_paths = [(data_dir / Path(*p), split) for p, split in label_file_paths]

        def _coco_importer(data_paths, label_file_path, set=0):
            coco = COCO(label_file_path)
            info = coco.dataset.get("info", {})
            licenses = coco.dataset.get("licenses", [])

            # 1. create all labels
            self.create_coco_labels(coco.cats.values())

            ann_by_task = {}
            # 2. get image full path and size
            for idx, img in coco.imgs.items():
                file_name = img["file_name"]
                img_path = filter(
                    lambda p: osp.normpath(p)[-len(osp.normpath(file_name)) :] == osp.normpath(file_name), data_paths
                )
                img_path = list(img_path)
                if len(img_path) != 1:
                    abort(
                        detail=f"{'No' if len(img_path) == 0 else 'Multiple'} image(s) with path ending with {file_name} found under {data_dir}",
                        status=404,
                    )

                img_path = img_path[0]
                data_paths.remove(img_path)
                coco.imgs[idx]["img_path"] = img_path
                coco.imgs[idx]["size"], _, _ = getSize(Path(data_dir) / img_path)
                ann_by_task[img["id"]] = []

            # 3. get ann by image
            for ann_id in coco.getAnnIds():
                ann = coco.anns[ann_id]
                if coco.imgs.get(ann["image_id"]) is None:
                    print(f"No image with id {ann['image_id']} found, skipping this annotation.")
                    continue

                label_name = coco.cats[ann["category_id"]]["name"]
                res = ann["segmentation"][0]
                width, height = (
                    coco.imgs[ann["image_id"]].get("width", None),
                    coco.imgs[ann["image_id"]].get("height", None),
                )
                for idx in range(0, len(res), 2):
                    res[idx] -= width / 2
                    res[idx + 1] -= height / 2

                res = [str(r) for r in res]
                res = ",".join(res)
                ann_by_task[ann["image_id"]].append(
                    {
                        "label_name": label_name,
                        "result": res,
                        "type": "polygon",
                        "frontend_id": len(ann_by_task[ann["image_id"]]) + 1,
                    }
                )

            # 4. add tasks
            for img_id, annotations in list(ann_by_task.items()):
                data_path = coco.imgs[img_id]["img_path"]
                self.add_task([{"path": data_path, "size": coco.imgs[img_id]["size"]}], [annotations], split=set)
            return data_paths, json.dumps({"info": info, "licenses": licenses})

        # 2. find all images under data_dir
        data_paths = listdir(data_dir, filters=filters)
        coco_others = {}
        for label_file_path, split_idx in label_file_paths:
            if label_file_path.exists():
                data_paths, others = _coco_importer(data_paths, label_file_path, split_idx)
                coco_others[split_idx] = others

        other_settings = project._get_other_settings()
        other_settings["coco_others"] = coco_others
        project.other_settings = json.dumps(other_settings)

        # 3. add tasks without label
        for data_path in data_paths:
            size, _, _ = getSize(data_dir / data_path)
            self.add_task([{"path": data_path, "size": size}])

        self.commit()

    def coco_exporter(self, export_dir):
        # 1. set params
        project = self.project

        # 2. create coco with all tasks
        coco = COCO()
        # 2.1 add categories
        labels = Label._get(project_id=project.project_id, many=True)
        for label in labels:
            if label.super_category_id is None:
                super_category_name = "none"
            else:
                super_category_name = self.label_id2name(label.super_category_id)
            coco.addCategory(label.id, label.name, label.color, super_category_name)

        # 2.2 add images
        split = [set(), set(), set()]
        tasks = Task._get(project_id=project.project_id, many=True)
        data_dir = osp.join(export_dir, "image")
        create_dir(data_dir)
        for task in tasks:
            data = task.datas[0]
            size = data.size.split(",")
            export_path = osp.join("image", osp.basename(data.path))
            coco.addImage(export_path, int(size[1]), int(size[2]), data.data_id)
            copy(osp.join(project.data_dir, data.path), data_dir)
            split[task.set].add(data.data_id)

        # 2.3 add annotations
        annotations = Annotation._get(project_id=project.project_id, many=True)
        for ann in annotations:
            if ann.type != "polygon":
                continue

            r = ann.result.split(",")
            r = [float(t) for t in r]
            width, height = (
                coco.imgs[ann.data_id]["width"],
                coco.imgs[ann.data_id]["height"],
            )
            width = int(width)
            height = int(height)
            for idx in range(0, len(r), 2):
                r[idx] += width / 2
                r[idx + 1] += height / 2

            coco.addAnnotation(
                ann.data_id,
                ann.label.id,
                segmentation=[r],
                id=ann.annotation_id,
            )

        # 3. write coco json
        coco_others = project._get_other_settings().get("coco_others", {})
        for split_idx, fname in enumerate(["train.json", "val.json", "test.json"]):
            outcoco = deepcopy(coco)
            outcoco.dataset["images"] = [img for img in coco.dataset["images"] if img["id"] in split[split_idx]]
            outcoco.dataset["annotations"] = [
                ann for ann in coco.dataset["annotations"] if ann["image_id"] in split[split_idx]
            ]

            coco_others_split = coco_others.get(str(split_idx), "{}")
            coco_others_split = json.loads(coco_others_split)

            outcoco.dataset["info"] = coco_others_split.get("info", "")
            outcoco.dataset["licenses"] = coco_others_split.get("licenses", [])

            with open(osp.join(export_dir, fname), "w") as outf:
                print(json.dumps(outcoco.dataset), file=outf)

    def eiseg_importer(
        self,
        data_dir=None,
        filters={"exclude_prefix": ["."], "include_postfix": image_extensions},
    ):
        project = self.project
        if data_dir is None:
            data_dir = project.data_dir
        data_dir = Path(data_dir)
        data_paths = [Path(p) for p in listdir(data_dir, filters=filters)]
        json_paths = listdir(data_dir, filters={"exclude_prefix": ["."], "include_postfix": [".json"]})
        json_paths = [Path(p) for p in json_paths]

        for data_path in data_paths:
            size, height, width = getSize(data_dir / data_path)
            json_path = match_by_base_name(data_path, json_paths)

            if len(json_path) == 0:
                self.add_task([{"path": str(data_path), "size": size}])
            else:
                json_path = json_path[0]
                anns_d = json.loads((data_dir / json_path).read_text())
                anns = []
                for ann in anns_d:
                    # ['name', 'labelIdx', 'color', 'points']
                    res = [wh for p in ann["points"] for wh in p]
                    for idx in range(0, len(res), 2):
                        res[idx] -= width / 2
                        res[idx + 1] -= height / 2
                    anns.append(
                        {
                            "label_name": ann["name"],
                            "result": ",".join(str(r) for r in res),
                            "type": "polygon",
                            "frontend_id": len(anns),
                        }
                    )
                self.add_task([{"path": str(data_path), "size": size}], [anns])
                json_paths.remove(json_path)
        self.commit()
