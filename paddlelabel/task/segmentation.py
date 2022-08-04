import os.path as osp
import json
from copy import deepcopy

import tifffile as tif
import numpy as np
import cv2
from pycocotoolse.coco import COCO

from paddlelabel.task.util import create_dir, listdir, image_extensions
from paddlelabel.task.base import BaseTask
from paddlelabel.config import db
from paddlelabel.task.util.color import hex_to_rgb
from paddlelabel.task.util import copy
from paddlelabel.api.model import Task, Label, Annotation
from paddlelabel.api.util import abort
from paddlelabel.api.rpc.seg import polygon2points

# debug
# import matplotlib
# matplotlib.use("TkAgg")
# import matplotlib.pyplot as plt


def draw_mask(data, type="pesudo"):
    height, width = map(int, data.size.split(",")[1:3])
    if type == "pesudo":
        mask = np.zeros((height, width, 3))
    else:
        mask = np.zeros((height, width))

    for ann in data.annotations:
        if ann.type != "brush":
            continue

        # TODO: remove
        if ann.result[:2] == "[[":
            continue

        label_id = ann.label.id
        result = ann.result.strip().split(",")
        try:
            result = [int(float(p)) for p in result]
        except:
            print(result, "to float error, plz open an issue for this")
        if ann.type == "brush":
            points = result[2:]
            line_width = result[0]
            if result[1] == 0:
                frontend_id = 0
                label_id = 0
            prev_w, prev_h = points[0:2]
        else:
            for idx in range(0, len(result), 2):
                result[idx] = int(result[idx] + width / 2)
                result[idx + 1] = int(result[idx + 1] + height / 2)
            points = polygon2points(result)
            points = np.array(points).reshape((-1))
            line_width = 1
            prev_w, prev_h = points[0:2]
        try:
            for idx in range(2, len(points), 2):
                w, h = points[idx : idx + 2]
                if type == "pesudo":
                    color = hex_to_rgb(ann.label.color)[::-1]
                else:
                    color = int(label_id)
                if line_width == 0:
                    line_width = 1
                cv2.line(mask, (prev_w, prev_h), (w, h), color, line_width)
                prev_w, prev_h = w, h
        except Exception as e:
            abort(detail=e.msg, status=500, title="cv2 error")
    return mask


def parse_semantic_mask(annotation_path, labels):
    ann = cv2.imread(annotation_path, cv2.IMREAD_UNCHANGED)
    frontend_id = 1
    anns = []
    # TODO: len(ann.shape == 3) and ann.shape[-1] == 1 necessary?
    # print(labels)
    if len(ann.shape) == 3:
        ann = cv2.cvtColor(ann, cv2.COLOR_BGR2RGB)
        ann_gray = np.zeros(ann.shape[:2], dtype="uint8")
        for label in labels:
            color = hex_to_rgb(label.color)
            label_mask = np.all(ann == color, axis=2)
            ann_gray[label_mask == 1] = label.id
            ann[label_mask == 1] = 0

        if ann.sum() != 0:
            ann = ann.reshape((-1, ann.shape[-1]))
            abort(
                f"Mask {annotation_path} contains unspecified labels {np.unique(ann, axis=0)[1:].tolist()} . Maybe you didn't include a background class in the first line of labels.txt or didn't specify label color?",
                404,
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
            result = f"{1},{frontend_id}," + result
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
        print(msg)
        abort(msg, 404)

    s = [1] + list(ann.shape)
    s = [str(s) for s in s]
    size = ",".join(s)
    return size, anns


def parse_instance_mask(annotation_path, labels):
    mask = tif.imread(annotation_path)
    instance_mask = mask[0]
    label_mask = mask[1]
    anns = []

    for label in labels:
        instance_part = instance_mask[label_mask == label.id]
        instance_ids = np.unique(instance_part)
        for instance_id in instance_ids:
            h, w = np.where(instance_mask == instance_id)
            result = ",".join([f"{w},{h}" for w, h in zip(w, h)])
            result = f"{1},{instance_id}," + result
            anns.append(
                {
                    "label_name": label.name,
                    "result": result,
                    "type": "brush",
                    "frontend_id": str(instance_id),
                }
            )
    s = [1] + list(instance_mask.shape)
    s = [str(s) for s in s]
    size = ",".join(s)
    return size, anns


class InstanceSegmentation(BaseTask):
    def __init__(self, project, data_dir=None):
        super().__init__(project, skip_label_import=True, data_dir=data_dir)
        self.importers = {
            "mask": self.mask_importer,
            "polygon": self.coco_importer,
        }
        self.exporters = {
            "mask": self.mask_exporter,
            "polygon": self.coco_exporter,
        }
        self.default_importer = self.coco_importer
        self.default_exporter = self.coco_exporter

    def mask_importer(
        self,
        data_dir=None,
        filters={"exclude_prefix": ["."], "include_postfix": image_extensions},
    ):
        # 1. set params
        project = self.project
        if data_dir is None:
            # base_dir = project.data_dir
            data_dir = project.data_dir
            # data_dir = osp.join(base_dir, "JPEGImages")
            # ann_dir = osp.join(base_dir, "Annotations")

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
                ann_path = osp.join(ann_dir, ann_dict[id])
                size, anns = parse_instance_mask(ann_path, project.labels)
            else:
                anns = []
                img = cv2.imread(data_path)
                s = [1] + list(img.shape)
                size = ",".join([str(s) for s in s])

            self.add_task([{"path": data_path, "size": size}], [anns])
        db.session.commit()

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
            height, width = map(int, data.size.split(",")[1:3])

            instance_mask = np.zeros((height, width), dtype="uint8")
            label_mask = np.zeros((height, width), dtype="uint8")
            for ann in task.annotations:

                # TODO: skip eiseg result, remove this
                if ann.result[:2] == "[[":
                    continue

                label_id = ann.label.id
                frontend_id = ann.frontend_id
                result = ann.result.split(",")
                try:
                    result = [int(float(p)) for p in result]
                except:
                    print(result, "to float error, plz open an issue for this")
                if ann.type == "brush":
                    points = result[2:]
                    line_width = result[0]
                    if result[1] == 0:
                        frontend_id = 0
                        label_id = 0
                    prev_w, prev_h = points[0:2]
                else:
                    for idx in range(0, len(result), 2):
                        result[idx] = int(result[idx] + width / 2)
                        result[idx + 1] = int(result[idx + 1] + height / 2)
                    points = polygon2points(result)
                    points = np.array(points).reshape((-1))
                    line_width = 1
                    prev_w, prev_h = points[0:2]
                try:
                    for idx in range(2, len(points), 2):
                        w, h = points[idx : idx + 2]
                        if line_width == 0:
                            line_width = 1

                        cv2.line(
                            label_mask,
                            (prev_w, prev_h),
                            (w, h),
                            int(label_id),
                            line_width,
                        )
                        cv2.line(
                            instance_mask,
                            (prev_w, prev_h),
                            (w, h),
                            int(frontend_id),
                            line_width,
                        )
                        prev_w, prev_h = w, h
                except Exception as e:
                    abort(detail=e.msg, status=500, title="cv2 error")

            mask = np.stack([instance_mask, label_mask], axis=0)
            tif.imwrite(export_label_path, mask, compression="zlib")

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
        if background_line is None or len(background_line) == 0:
            background_line = "background"
        self.export_labels(export_dir, background_line, with_id=True)

    def coco_importer(
        self,
        data_dir=None,
        filters={"exclude_prefix": ["."], "include_postfix": image_extensions},
    ):
        # 1. set params
        project = self.project
        if data_dir is None:
            data_dir = project.data_dir
        label_file_paths = ["train.json", "val.json", "test.json"]
        label_file_paths = [osp.join(data_dir, f) for f in label_file_paths]

        self.create_warning(data_dir)

        def _coco_importer(data_paths, label_file_path, set=0):
            coco = COCO(label_file_path)
            info = coco.dataset.get("info", {})
            licenses = coco.dataset.get("licenses", [])

            # 1. create all labels
            self.create_coco_labels(coco.cats.values())

            print("=====", data_paths)
            ann_by_task = {}
            # 2. get image full path and size
            for idx, img in coco.imgs.items():
                file_name = img["file_name"]
                full_path = filter(
                    lambda p: osp.normpath(p)[-len(osp.normpath(file_name)) :] == osp.normpath(file_name), data_paths
                )
                full_path = list(full_path)
                if len(full_path) != 1:
                    abort(
                        detail=f"{'No' if len(full_path) == 0 else 'Multiple'} image(s) with path ending with {file_name} found under {data_dir}",
                        status=404,
                    )

                full_path = full_path[0]
                data_paths.remove(full_path)
                coco.imgs[idx]["full_path"] = full_path
                s = [img.get("height", 0), img.get("width", 0)]
                if s == [0, 0]:
                    s = cv2.imread(full_path).shape[:2]
                s = [str(t) for t in s]
                coco.imgs[idx]["size"] = ",".join(s)
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
                data_path = coco.imgs[img_id]["full_path"]
                size = "1," + coco.imgs[img_id]["size"]
                self.add_task([{"path": data_path, "size": size}], [annotations], split=set)
            return data_paths, json.dumps({"info": info, "licenses": licenses})

        # 2. find all images under data_dir
        data_paths = listdir(data_dir, filters=filters)
        coco_others = {}
        for split_idx, label_file_path in enumerate(label_file_paths):
            if osp.exists(label_file_path):
                data_paths, others = _coco_importer(data_paths, label_file_path, split_idx)
                coco_others[split_idx] = others
        other_settings = project._get_other_settings()
        other_settings["coco_others"] = coco_others
        project.other_settings = json.dumps(other_settings)

        # 3. add tasks without label
        for data_path in data_paths:
            img = cv2.imread(osp.join(data_dir, data_path))
            s = img.shape
            size = [1, s[1], s[0], s[2]]
            size = [str(s) for s in size]
            size = ",".join(size)
            self.add_task([{"path": data_path, "size": size}])

        db.session.commit()

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
                segmentation=r,
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


class SemanticSegmentation(InstanceSegmentation):
    def __init__(self, project, data_dir=None):
        super().__init__(project, data_dir=data_dir)
        self.importers = {
            "mask": self.mask_importer,
            "polygon": self.coco_importer,
        }
        self.exporters = {
            "mask": self.mask_exporter,
            "polygon": self.coco_exporter,
        }
        self.default_importer = self.mask_importer
        self.default_exporter = self.mask_exporter

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

        background_line = self.import_labels(ignore_first=True)
        other_settings = project._get_other_settings()
        other_settings["background_line"] = background_line
        project.other_settings = json.dumps(other_settings)

        ann_dict = {osp.basename(p).split(".")[0]: p for p in listdir(ann_dir, filters)}

        # 2. import records
        for data_path in listdir(data_dir, filters):
            id = osp.basename(data_path).split(".")[0]
            data_path = osp.join(data_dir, data_path)
            if id in ann_dict.keys():
                ann_path = osp.join(ann_dir, ann_dict[id])
                size, anns = parse_semantic_mask(ann_path, project.labels)
            else:
                anns = []
                img = cv2.imread(data_path)
                s = [1] + list(img.shape)
                size = ",".join([str(s) for s in s])

            self.add_task([{"path": data_path, "size": size}], [anns])
        db.session.commit()

    def mask_exporter(self, export_dir: str, type: str = "gray"):
        """Export semantic segmentation dataset in mask format

        Args:
            export_dir (str): The folder to export to.
            type (str, optional): Mask type, "gray" or "pesudo". Defaults to "gray".
        """

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
            export_label_path = osp.join(export_label_dir, osp.basename(data_path).split(".")[0] + ".png")

            copy(data_path, export_data_dir)

            mask = draw_mask(data, type=type)
            cv2.imwrite(export_label_path, mask)

            export_data_paths.append([export_data_path])
            export_label_paths.append([export_label_path])

        self.export_split(
            export_dir,
            tasks,
            export_data_paths,
            with_labels=False,
            annotation_ext=".png",
        )
        bg = project._get_other_settings().get("background_line", "background")
        self.export_labels(export_dir, bg)


"""
{
            "id": 2,
            "name": "toy",
            "color": "#64F3BE",
            "supercategory": "none"
        },
"""
