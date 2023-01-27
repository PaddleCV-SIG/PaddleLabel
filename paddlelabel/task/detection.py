# -*- coding: utf-8 -*-
from __future__ import annotations

import os.path as osp
from pathlib import Path
import json
from copy import deepcopy

from pycocotoolse.coco import COCO

from paddlelabel.api import Task, Annotation, Label
from paddlelabel.task.util import (
    create_dir,
    listdir,
    copy,
    image_extensions,
    ensure_unique_base_name,
    get_fname,
    break_path,
)
from paddlelabel.task.base import BaseTask
from paddlelabel.io.image import getSize

# TODO: move to io
def parse_voc_label(label_path):
    from xml.dom import minidom

    def data(elements):
        if elements[0].firstChild is not None:
            return elements[0].firstChild.data
        return ""

    file = minidom.parse(label_path)

    # 1. parse img info
    img = {}

    # 1.1 file path
    folder = file.getElementsByTagName("folder")
    folder = "JPEGImages" if len(folder) == 0 else data(folder)
    filename = file.getElementsByTagName("filename")
    filename = "" if len(filename) == 0 else data(filename)
    # if len(filename) == 0:
    #     raise RuntimeError(f"Missing required field filename in annotation file {label_path}")
    path = osp.join(folder, filename)

    # 1.2 size
    size = file.getElementsByTagName("size")[0]
    size = [data(size.getElementsByTagName(n)) for n in ["height", "width"]]
    height, width = [int(t) for t in size]
    size = [str(t) for t in [1, height, width]]

    img["size"] = ",".join(size)
    img["path"] = path

    # 2. parse annotations
    objects = file.getElementsByTagName("object")
    anns = []
    frontend_id = 1
    for object in objects:
        ann = {}
        ann["label_name"] = data(object.getElementsByTagName("name"))
        bndbox = object.getElementsByTagName("bndbox")[0]
        # ann["result"] = {}
        # ann["result"]["xmin"] = data(bndbox.getElementsByTagName("xmin"))
        # ann["result"]["xmax"] = data(bndbox.getElementsByTagName("xmax"))
        # ann["result"]["ymin"] = data(bndbox.getElementsByTagName("ymin"))
        # ann["result"]["ymax"] = data(bndbox.getElementsByTagName("ymax"))
        # ann["result"] = json.dumps(ann["result"])
        names = ["xmin", "ymin", "xmax", "ymax"]
        r = [data(bndbox.getElementsByTagName(n)) for n in names]
        r = [float(t) for t in r]
        r[0] -= width / 2
        r[1] -= height / 2
        r[2] -= width / 2
        r[3] -= height / 2
        r = [str(t) for t in r]
        ann["result"] = ",".join(r)
        ann["type"] = "rectangle"
        ann["frontend_id"] = frontend_id
        anns.append(ann)
        frontend_id += 1
    return img, anns


def create_voc_label(filepath, width, height, annotations):
    object_labels = ""
    width = int(float(width))
    height = int(float(height))
    for ann in annotations:
        r = [float(t) for t in ann.result.split(",")]
        r[0] += width / 2
        r[1] += height / 2
        r[2] += width / 2
        r[3] += height / 2
        r = [int(t) for t in r]

        object_labels += f"""
            <object>
            <name>{ann.label.name}</name>
            <bndbox>
            <xmin>{r[0]}</xmin>
            <ymin>{r[1]}</ymin>
            <xmax>{r[2]}</xmax>
            <ymax>{r[3]}</ymax>
            </bndbox>
            </object>
        """

    folder = osp.dirname(filepath)
    filename = osp.basename(filepath)
    voc_label = f"""
        <?xml version='1.0' encoding='UTF-8'?>
        <annotation>
        <folder>{folder}</folder>
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
    # from xml.dom import minidom
    # return minidom.parseString(voc_label.strip()).toprettyxml(indent="    ", newl="")
    return voc_label.strip()


# TODO: change data_dir to dataset_path


class Detection(BaseTask):
    def __init__(self, *args, **kwargs):
        super(Detection, self).__init__(*args, **kwargs)
        self.importers = {
            "coco": self.coco_importer,
            "voc": self.voc_importer,
            "yolo": self.yolo_importer,
        }
        self.exporters = {
            "coco": self.coco_exporter,
            "voc": self.voc_exporter,
            "yolo": self.yolo_exporter,
        }
        self.default_exporter = self.voc_exporter

    def to_easydata(self, project_id, access_token, dataset_id):
        import concurrent.futures
        from threading import Lock
        from queue import Queue
        import time
        import base64
        import requests

        # print(project_id, dataset_id, access_token)
        # print(type(dataset_id))
        # TODO: option to create new dataset

        # TODO: list datasets to ensure datasetid exists
        # host = f'https://aip.baidubce.com/rpc/2.0/easydl/dataset/list?access_token={access_token}'
        # response = requests.post(host, json={"type": "OBJECT_DETECTION"})
        # print(response)
        # if response:
        #     print(response.json())

        project = self.project
        host = f"https://aip.baidubce.com/rpc/2.0/easydl/dataset/addentity?access_token={access_token}"
        base_body = {
            "type": "OBJECT_DETECTION",
            "dataset_id": dataset_id,
            "appendLabel": False,
        }

        tasks = Queue()
        for task in Task._get(project_id=project_id, many=True):
            tasks.put(task)

        def upload(task):
            tic = time.time()
            body = base_body.copy()
            data = task.datas[0]
            body["entity_name"] = Path(data.path).name
            img_path = Path(project.data_dir) / data.path
            with open(Path(project.data_dir) / data.path, "rb") as f:
                img = f.read()
                body["entity_content"] = base64.b64encode(img).decode("utf-8")
            if len(task.annotations) != 0:
                labels = []
                h, w = list(map(int, data.size.split(",")))[1:3]
                h /= 2
                w /= 2
                for ann in task.annotations:
                    fi = lambda v: int(float(v))
                    bb = list(map(fi, ann.result.split(",")))
                    labels.append(
                        {
                            "label_name": ann.label.name,
                            "left": bb[0] + w,
                            "top": bb[1] + h,
                            "width": bb[2] - bb[0],
                            "height": bb[3] - bb[1],
                        }
                    )
                body["labels"] = labels
            res = requests.post(host, json=body)
            res_json = res.json()
            # print("\t", task.task_id, res_json, len(res_json.keys()) == 1, time.time() - tic)
            return len(res_json.keys()) == 1 and res.status_code == 200, task

        # while not tasks.empty():
        #     upload(tasks.get())

        tot = tasks.qsize()
        finished = 0
        upload_trials = 0
        success_lock = Lock()

        with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:

            def retry_failed(future):
                nonlocal finished, tasks
                success, task = future.result()
                if success:
                    with success_lock:
                        finished += 1
                else:
                    tasks.put(task)

            while not tasks.empty():
                print(f"{finished} / {tot} , {(finished/tot)*100:.1f}%")
                upload_trials += 1
                future = executor.submit(upload, tasks.get())
                future.add_done_callback(retry_failed)
                time.sleep(1)

            while finished < 10:
                print(finished)
                time.sleep(1)

            print(finished, upload_trials, upload_trials / finished)

    def yolo_importer(
        self,
        data_dir=None,
        filters={"exclude_prefix": ["."], "include_postfix": image_extensions},
    ):
        # 1. set params
        project = self.project
        data_dir = Path(project.data_dir if data_dir is None else data_dir)

        # 2. get all data and labels, ensure all data basename unique
        data_paths = listdir(data_dir, filters=filters)
        label_paths = listdir(
            data_dir, filters={"exclude_prefix": [".", "labels.txt", "classes.txt"], "include_postfix": [".txt"]}
        )
        label_paths = [Path(p) for p in label_paths]

        ensure_unique_base_name([data_dir / p for p in data_paths])
        data_paths = map(Path, data_paths)

        label_dict = {}
        for label_path in label_paths:
            label_dict[label_path.name.split(".")[0]] = label_path

        for data_path in data_paths:
            basename = data_path.name.split(".")[0]
            size, height, width = getSize(data_dir / data_path)
            ann_list = []

            if basename in label_dict.keys():
                # print(project.labels)
                anns = (data_dir / label_dict[basename]).read_text().strip().split("\n")
                anns = [a.strip().split(" ") for a in anns]
                anns = [[float(num) for num in ann] for ann in anns if ann != ""]

                for fid, ann in enumerate(anns):
                    xmid, ymid, xlen, ylen = ann[1:]
                    res = [xmid - xlen / 2, ymid - ylen / 2, xmid + xlen / 2, ymid + ylen / 2]
                    # if any(map(lambda v: v > 1.1, ann[1:])):  # whether normalized position
                    #     res[0] -= width / 2
                    #     res[1] -= height / 2
                    #     res[2] -= width / 2
                    #     res[3] -= height / 2
                    # else:
                    res = [r - 0.5 for r in res]
                    res[0] *= width
                    res[1] *= height
                    res[2] *= width
                    res[3] *= height
                    res = ",".join(map(str, res))
                    ann_list.append(
                        {
                            "label_name": self.label_id2name(ann[0] + 1),
                            "result": res,
                            "type": "rectangle",
                            "frontend_id": fid + 1,
                        }
                    )
            # print(ann_list)
            self.add_task([{"path": str(data_path), "size": size}], [ann_list])
        self.commit()

    def yolo_exporter(self, export_dir):
        # BUG: if the labels ids are not continuos
        # 1. set params
        project = self.project

        export_data_dir = osp.join(export_dir, "JPEGImages")
        export_label_dir = osp.join(export_dir, "Annotations")
        create_dir(export_data_dir)
        create_dir(export_label_dir)

        label_id_mapping = self.export_labels(osp.join(export_dir, "classes.names"))

        tasks = Task._get(project_id=project.project_id, many=True)
        export_paths = []

        for task in tasks:
            data = task.datas[0]
            data_path = osp.join(project.data_dir, data.path)
            export_path = osp.join("JPEGImages", osp.basename(data.path))
            copy(data_path, export_data_dir)

            height, width = map(int, data.size.split(",")[1:3])
            yolo_res = ""
            for ann in task.annotations:
                r: list[float] = [float(t) for t in ann.result.split(",")]
                res = [0.0 for _ in range(4)]
                res[0] = r[0] / width + 0.5
                res[1] = r[1] / height + 0.5
                res[2] = (r[2] - r[0]) / width
                res[3] = (r[3] - r[1]) / height
                res[0] += res[2] / 2
                res[1] += res[3] / 2
                # print(ann.label.id)
                yolo_res += f"{label_id_mapping[ann.label.id]} {' '.join(map(str, res))}\n"
            if yolo_res != "":
                with open(
                    osp.join(export_dir, "Annotations", osp.basename(data.path).split(".")[0] + ".txt"), "w"
                ) as f:
                    print(yolo_res, file=f, end="")

            export_paths.append([export_path])

        self.export_split(export_dir, tasks, export_paths, with_labels=False, annotation_ext=".txt")

    def coco_importer(
        self,
        data_dir: Path | None = None,
        filters={"exclude_prefix": ["."], "include_postfix": image_extensions},
    ):
        """
        images should be located at data_dir / file_name in coco annotation
        """

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
            (["label", "COCO", "annotations.json"], 0),  # EISeg format
        ]
        label_file_paths = [(data_dir / Path(*p), split) for p, split in label_file_paths]

        def _coco_importer(data_paths, label_file_path, set=0):
            coco = COCO(label_file_path)
            info = coco.dataset.get("info", {})
            licenses = coco.dataset.get("licenses", [])

            # 1. create all labels
            self.create_coco_labels(coco.cats.values())

            ann_by_task = {}
            """
            2. for each image record in coco annotation, get image full path and size
                - match image record and image file path on disk by image name
                - annotation records that dont't have matching image file on disk will be discarded
                - all images under data dir will be imported
            """
            for idx, img in coco.imgs.items():
                file_name = get_fname(img["file_name"])
                data_path = list(filter(lambda p: str(p)[-len(file_name) :] == file_name, data_paths))
                # multiple match cause import failure
                if len(data_path) > 1:
                    raise RuntimeError(f"Multiple image(s) with path ending with {file_name} found under {data_dir}")
                # no matching record on disk, this image record will be skipped
                if len(data_path) == 0:
                    continue
                data_path = data_path[0]
                data_paths.remove(data_path)
                coco.imgs[idx]["data_path"] = data_path
                # s = [img.get("height", None), img.get("width", None)]
                # if s == [None, None]:
                size, height, width = getSize(data_dir / data_path)
                coco.imgs[idx]["height"], coco.imgs[idx]["width"] = height, width

                coco.imgs[idx]["size"] = size
                ann_by_task[img["id"]] = []

            # 3. get ann by image
            for ann_id in coco.getAnnIds():
                ann = coco.anns[ann_id]
                # if the image this ann belongs to isn't found on disk, skip this ann
                if ann["image_id"] not in ann_by_task.keys():
                    continue
                label_name = coco.cats[ann["category_id"]]["name"]
                # result = {}
                # result["xmin"] = ann["bbox"][0]
                # result["ymin"] = ann["bbox"][1]
                # result["xmax"] = result["xmin"] + ann["bbox"][2]
                # result["ymax"] = result["ymin"] + ann["bbox"][3]

                # image center as origin, right x down y
                res = ann["bbox"]
                height, width = (coco.imgs[ann["image_id"]]["height"], coco.imgs[ann["image_id"]]["width"])
                res[2] += res[0]
                res[3] += res[1]
                res[0] -= width / 2
                res[1] -= height / 2
                res[2] -= width / 2
                res[3] -= height / 2

                res = [str(r) for r in res]
                res = ",".join(res)
                ann_by_task[ann["image_id"]].append(
                    {
                        "label_name": label_name,
                        "result": res,
                        "type": "rectangle",
                        "frontend_id": len(ann_by_task[ann["image_id"]]) + 1,
                    }
                )

            # 4. add tasks
            for img_id, annotations in list(ann_by_task.items()):
                data_path = coco.imgs[img_id]["data_path"]
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
            size, _, _ = getSize(Path(data_dir) / data_path)
            self.add_task([{"path": data_path, "size": size}])

        self.commit()

    def coco_exporter(self, export_dir, allow_empty=True):
        # 1. set params
        project = self.project

        # 2. create coco with all tasks
        coco = COCO()
        # 2.1 add categories
        labels = Label._get(project_id=project.project_id, many=True)
        for label in labels:
            coco.addCategory(
                label.id,
                label.name,
                label.color,
                None if label.super_category_id is None else self.label_id2name(label.super_category_id),
            )

        # 2.2 add images
        split = [set(), set(), set()]
        tasks = Task._get(project_id=project.project_id, many=True)
        data_dir = osp.join(export_dir, "image")
        create_dir(data_dir)
        for task in tasks:
            data = task.datas[0]
            if not allow_empty and len(data.annotations) == 0:
                continue

            size = data.size.split(",")
            export_path = osp.basename(data.path)
            coco.addImage(export_path, int(size[2]), int(size[1]), data.data_id)
            copy(osp.join(project.data_dir, data.path), data_dir)
            split[task.set].add(data.data_id)

        # 2.3 add annotations
        annotations = Annotation._get(project_id=project.project_id, many=True)
        for ann in annotations:
            r = ann.result.split(",")
            r = [float(t) for t in r]
            width, height = (
                coco.imgs[ann.data_id]["width"],
                coco.imgs[ann.data_id]["height"],
            )
            width = int(width)
            height = int(height)
            bb = [
                r[0] + width / 2,
                r[1] + height / 2,
                r[2] + width / 2,
                r[3] + height / 2,
            ]
            bb[0], bb[2] = (bb[0], bb[2]) if bb[0] < bb[2] else (bb[2], bb[0])
            bb[1], bb[3] = (bb[1], bb[3]) if bb[1] < bb[3] else (bb[3], bb[1])
            bb[2] -= bb[0]
            bb[3] -= bb[1]
            coco.addAnnotation(
                ann.data_id,
                ann.label.id,
                segmentation=[],
                id=ann.annotation_id,
                bbox=bb,
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

    def voc_importer(
        self,
        data_dir: Path | None = None,
        filters={"exclude_prefix": ["."], "include_postfix": image_extensions},
    ) -> None:
        """
        Import voc format detection dataset

        Parameters
        ----------
        data_dir : Path | None, optional
            Dataset folder path. Defaults to None
        filters : dict, optional
            Pattern used to search for images by file names. Defaults to {"exclude_prefix": ["."], "include_postfix": image_extensions}

        Raises
        ------
        RuntimeError
            Failed to match an annotation to an image.
        """
        # 1. set params
        project = self.project
        data_dir = Path(project.data_dir if data_dir is None else data_dir)
        self.create_warning(data_dir)

        # 2. get all data and label
        data_paths = set(listdir(data_dir, filters=filters))
        label_paths = listdir(data_dir, filters={"exclude_prefix": ["."], "include_postfix": [".xml"]})
        label_paths = list(map(Path, label_paths))

        # 2.1 get match from xx_list.txt
        list_files = ["train_list.txt", "val_list.txt", "test_list.txt"]
        list_mappings = {}
        for list_file in list_files:
            list_file_path = data_dir / list_file
            if not list_file_path.exists():
                continue
            pairs = list_file_path.read_text(encoding="utf-8").split("\n")
            pairs = [list(map(break_path, p.strip().split(" "))) for p in pairs if len(p.strip()) != 0]
            list_mappings.update({Path(*p[1]): Path(*p[0]) for p in pairs})

        name_mappings = {}
        data_paths_m = {Path(p).name.split(".")[0]: Path(p) for p in data_paths}
        for label_path in label_paths:
            base_name = label_path.name.split(".")[0]
            name_mappings[label_path] = data_paths_m.get(base_name, None)

        for label_path in label_paths:
            data, labels = parse_voc_label(osp.join(data_dir, label_path))
            data_path = list_mappings.get(label_path, None)
            if data_path is None:
                data_path = name_mappings.get(label_path, None)
            if data_path is None:
                data_path = Path(data["path"])
            data["path"] = str(data_path)
            data_path = data_dir / data_path

            if not data_path.exists():
                raise RuntimeError(
                    f"Image specified in label xml file {str(label_path)} not found at {str(data_path)}."
                )

            size, _, _ = getSize(data_path)

            # def wxh(size):
            #     return "x".join(size.split(",")[1:3])

            # if wxh(size) != wxh(data["size"]):
            #     log.error(
            #         f"Image size got by reading image: {wxh(size)} isn't the same as parsed from pascal xml({label_path}): {wxh(data['size'])}"
            #     )
            #     # log.error(f"{size} vs {data['size']}")
            #     data["size"] = size

            self.add_task([data], [labels])
            data_paths.remove(data["path"])  # TODO: change to Path

        for data_path in data_paths:
            size, _, _ = getSize(Path(data_dir) / data_path)
            self.add_task([{"path": data_path, "size": size}])

        self.commit()

    def voc_exporter(self, export_dir):
        # 1. set params
        project = self.project

        export_data_dir = osp.join(export_dir, "JPEGImages")
        export_label_dir = osp.join(export_dir, "Annotations")
        create_dir(export_data_dir)
        create_dir(export_label_dir)

        self.export_labels(osp.join(export_dir, "labels.txt"))

        tasks = Task._get(project_id=project.project_id, many=True)
        export_paths = []

        for task in tasks:
            data = task.datas[0]
            data_path = osp.join(project.data_dir, data.path)
            export_path = osp.join("JPEGImages", osp.basename(data.path))

            copy(data_path, export_data_dir)
            id = osp.basename(data_path).split(".")[0]
            height, width = data.size.split(",")[1:3]
            with open(osp.join(export_label_dir, f"{id}.xml"), "w", encoding="utf-8") as f:
                print(
                    create_voc_label(export_path, width, height, data.annotations),
                    file=f,
                )
            export_paths.append([export_path])

        self.export_split(export_dir, tasks, export_paths, with_labels=False, annotation_ext=".xml")
