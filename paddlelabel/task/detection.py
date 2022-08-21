import os.path as osp
import json
from copy import deepcopy
from pathlib import Path
import logging

from pycocotoolse.coco import COCO
import cv2

from paddlelabel.api import Task, Annotation, Label
from paddlelabel.task.util import create_dir, listdir, copy, image_extensions, ensure_unique_base_name
from paddlelabel.task.base import BaseTask
from paddlelabel.config import db
from paddlelabel.api.util import abort


log = logging.getLogger("PaddleLabel")


# TODO: move to io
def parse_voc_label(label_path):
    from xml.dom import minidom

    def data(elements):
        return elements[0].firstChild.data

    file = minidom.parse(label_path)

    # 1. parse img info
    img = {}

    # 1.1 file path
    folder = file.getElementsByTagName("folder")
    if len(folder) == 0:
        folder = "JPEGImages"
    else:
        folder = data(folder)
    filename = file.getElementsByTagName("filename")
    if len(filename) == 0:
        abort(detail=f"Missing required field filename in annotation file {label_path}", status=404)
    filename = data(filename)
    path = osp.join(folder, filename)

    # 1.2 size
    size = file.getElementsByTagName("size")[0]
    size = [data(size.getElementsByTagName(n)) for n in ["width", "height"]]
    width, height = [int(t) for t in size]
    size = [str(t) for t in [1, width, height]]

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
        r = [int(t) for t in r]
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
    width = int(width)
    height = int(height)
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
    def __init__(self, project, data_dir=None, is_export=False):
        super(Detection, self).__init__(project, data_dir=data_dir, is_export=is_export)
        self.importers = {"coco": self.coco_importer, "voc": self.voc_importer, "yolo": self.yolo_importer}
        self.exporters = {"coco": self.coco_exporter, "voc": self.voc_exporter, "yolo": self.yolo_exporter}
        self.default_importer = self.voc_importer
        self.default_exporter = self.voc_exporter  # default to voc

    def yolo_importer(self, data_dir=None, filters={"exclude_prefix": ["."], "include_postfix": image_extensions}):

        # 1. set params
        project = self.project
        if data_dir is None:
            data_dir = Path(project.data_dir)

        # 2. get all data and labels, ensure all data basename unique
        data_paths = listdir(data_dir, filters=filters)
        label_paths = listdir(data_dir, filters={"exclude_prefix": [".", "labels.txt"], "include_postfix": [".txt"]})
        label_paths = [Path(p) for p in label_paths]

        ensure_unique_base_name([data_dir / Path(p) for p in data_paths])
        data_paths = map(Path, listdir(data_dir, filters=filters))

        label_dict = {}
        for label_path in label_paths:
            label_dict[label_path.name.split(".")[0]] = label_path

        for data_path in data_paths:
            basename = data_path.name.split(".")[0]

            size = cv2.imread(str(data_dir / data_path), cv2.IMREAD_UNCHANGED).shape
            height, width = size[0], size[1]
            size = list(map(str, size))
            size[0], size[1] = size[1], size[0]
            size = "1," + ",".join(size)
            ann_list = []

            if basename in label_dict.keys():
                anns = (data_dir / label_dict[basename]).read_text().strip().split("\n")
                anns = [a.strip().split(" ") for a in anns]
                anns = [[float(num) for num in ann] for ann in anns if ann != ""]

                for fid, ann in enumerate(anns):
                    xmid, ymid, xlen, ylen = ann[1:]
                    res = [xmid - xlen / 2, ymid - ylen / 2, xmid + xlen / 2, ymid + ylen / 2]
                    res = [r - 0.5 for r in res]
                    res[0] *= width
                    res[1] *= height
                    res[2] *= width
                    res[3] *= height
                    res = ",".join(map(str, res))

                    ann_list.append(
                        {
                            "label_name": self.label_id2name(int(ann[0]) + 1),
                            "result": res,
                            "type": "rectangle",
                            "frontend_id": fid + 1,
                        }
                    )

            self.add_task([{"path": str(data_path), "size": size}], [ann_list])
        db.session.commit()

    def yolo_exporter(self, export_dir):
        # 1. set params
        project = self.project

        export_data_dir = osp.join(export_dir, "JPEGImages")
        export_label_dir = osp.join(export_dir, "Annotations")
        create_dir(export_data_dir)
        create_dir(export_label_dir)

        self.export_labels(osp.join(export_dir, "classes.names"))

        tasks = Task._get(project_id=project.project_id, many=True)
        export_paths = []

        for task in tasks:
            data = task.datas[0]
            data_path = osp.join(project.data_dir, data.path)
            export_path = osp.join("JPEGImages", osp.basename(data.path))
            copy(data_path, export_data_dir)

            width, height = map(int, data.size.split(",")[1:3])
            print(width, height)
            yolo_res = ""
            for ann in task.annotations:
                r = [float(t) for t in ann.result.split(",")]
                res = [0 for _ in range(4)]
                res[0] = r[0] / width + 0.5
                res[1] = r[1] / height + 0.5
                res[2] = (r[2] - r[0]) / width
                res[3] = (r[3] - r[1]) / height
                res[0] += res[2] / 2
                res[1] += res[3] / 2
                yolo_res += f"{ann.label.id - 1} {' '.join(map(str, res))}\n"
            if yolo_res != "":
                with open(
                    osp.join(export_dir, "Annotations", osp.basename(data.path).split(".")[0] + ".txt"), "w"
                ) as f:
                    print(yolo_res, file=f, end="")

            export_paths.append([export_path])

        self.export_split(export_dir, tasks, export_paths, with_labels=False, annotation_ext=".txt")

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
        label_file_paths = ["train.json", "val.json", "test.json"]
        label_file_paths = [osp.join(data_dir, f) for f in label_file_paths]

        self.create_warning(data_dir)

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
                full_path = filter(
                    lambda p: osp.normpath(p)[-len(osp.normpath(file_name)) :] == osp.normpath(file_name), data_paths
                )
                full_path = list(full_path)
                if len(full_path) != 1:
                    raise RuntimeError(
                        f"{'No' if len(full_path) == 0 else 'Multiple'} image(s) with path ending with {file_name} found under {data_dir}"
                    )
                full_path = full_path[0]
                data_paths.remove(full_path)
                coco.imgs[idx]["full_path"] = full_path
                s = [img.get("width", 0), img.get("height", 0)]
                if s == [0, 0]:
                    s = cv2.imread(full_path).shape[:2][::-1]
                s = [str(t) for t in s]
                coco.imgs[idx]["size"] = ",".join(s)
                ann_by_task[img["id"]] = []

            # 3. get ann by image
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
                # curr_anns = ann_by_task.get(ann["image_id"], [])
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
        data_dir=None,
        filters={"exclude_prefix": ["."], "include_postfix": image_extensions},
    ):
        # 1. set params
        project = self.project
        base_dir = data_dir
        allow_missing_image = data_dir is not None

        if base_dir is None:
            base_dir = project.data_dir
        self.create_warning(base_dir)

        # 2. get all data and label
        data_paths = set(p for p in listdir(base_dir, filters=filters))
        label_paths = [p for p in listdir(base_dir, filters={"exclude_prefix": ["."], "include_postfix": [".xml"]})]

        for label_path in label_paths:
            data, labels = parse_voc_label(osp.join(base_dir, label_path))
            img = cv2.imread(osp.join(base_dir, data["path"]))
            s = img.shape
            size = [1, s[1], s[0], s[2]]
            size = [str(s) for s in size]
            size = ",".join(size)
            if size != data["size"]:
                log.error(f"Image size read from disk {size} isn't the same with parsed from pascal xml {data['size']}")
                data["size"] = size
            if not osp.exists(osp.join(base_dir, data["path"])):
                if allow_missing_image:
                    continue
                else:
                    raise RuntimeError(f"Image specified in {label_path} not found.")
            self.add_task([data], [labels])
            data_paths.remove(data["path"])

        for data_path in data_paths:
            img = cv2.imread(osp.join(base_dir, data_path))
            s = img.shape
            size = [1, s[1], s[0], s[2]]
            size = [str(s) for s in size]
            size = ",".join(size)
            self.add_task([{"path": data_path, "size": size}])

        db.session.commit()

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
            width, height = data.size.split(",")[1:3]
            with open(osp.join(export_label_dir, f"{id}.xml"), "w") as f:
                print(
                    create_voc_label(export_path, width, height, data.annotations),
                    file=f,
                )
            export_paths.append([export_path])

        self.export_split(export_dir, tasks, export_paths, with_labels=False, annotation_ext=".xml")
