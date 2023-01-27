# -*- coding: utf-8 -*-
from __future__ import annotations
import os.path as osp
import json
from collections import defaultdict
from pathlib import Path

from paddlelabel.task.util import create_dir, listdir, image_extensions, match_by_base_name
from paddlelabel.task.base import BaseTask
from paddlelabel.task.util import copy
from paddlelabel.io.image import getSize
from paddlelabel.api.model import Task, Annotation, Project
from paddlelabel.api.util import abort


class OpticalCharacterRecognition(BaseTask):
    def __init__(
        self,
        project: Project,
        data_dir: Path | None = None,
        is_export: bool = False,
    ):
        super().__init__(project, skip_label_import=True, data_dir=data_dir, is_export=is_export)
        self.importers = {"json": self.json_importer, "txt": self.txt_importer}
        self.exporters = {"json": self.json_exporter, "txt": self.txt_exporter}
        self.default_exporter = self.txt_exporter
        # NOTE: ocr doesn't need a label but label is required field for annotation. thus use a dummy label
        self.dummy_label_name = "OCR Dummy Label"

    def encode_ann(self, ann: dict) -> dict[str, str]:
        res = ""
        for p in ann.get("points", []):
            res += "|".join(map(str, p)) + "|"
        if len(res) == 0:
            res += "no points|"
        res += "|"
        res += ann.get("transcription", "") + "|"
        res += str(int(ann.get("illegibility", False))) + "|"
        res += ann.get("language", "")
        return {
            "label_name": self.dummy_label_name,
            "result": res,
            "type": "ocr_polygon",
            "frontend_id": ann["frontend_id"],
            "predicted_by": "PaddleOCR",
        }

    def txt_importer(
        self,
        data_dir: Path | None = None,
        filters={"exclude_prefix": ["."], "include_postfix": image_extensions},
    ):
        project = self.project
        if data_dir is None:
            data_dir = project.data_dir
        data_dir = Path(data_dir)
        label_file_paths = {0: ["Label.txt", "train.txt"], 1: ["val.txt"], 2: ["test.txt"]}
        label_file_paths = {k: [data_dir / f for f in v] for k, v in label_file_paths.items()}

        self.create_warning(data_dir)
        self.add_label(
            self.dummy_label_name,
            comment="Dummy label for ocr project, added for compatibility, don't delete.",
            commit=True,
        )

        data_paths = set(Path(p) for p in listdir(data_dir, filters=filters))
        # print(data_paths)
        for set_idx in label_file_paths:
            for label_file_path in label_file_paths[set_idx]:
                if not label_file_path.exists():
                    continue
                labels = label_file_path.read_text(encoding="utf-8").split("\n")
                labels_d = {}
                for label in labels:
                    label = label.strip()
                    if len(label) == 0:
                        continue
                    img_path, anns = label.split("\t")
                    anns = json.loads(anns)
                    for idx in range(len(anns)):
                        anns[idx]["frontend_id"] = idx + 1

                    anns = [self.encode_ann(ann) for ann in anns]
                    labels_d[img_path] = anns

                label_fnames = set(labels_d.keys())
                imported_data_path = set()
                for data_path in data_paths:
                    label_fname = match_by_base_name(data_path, label_fnames)
                    if len(label_fname) == 0:
                        continue
                    label_fname = str(label_fname[0])
                    size, height, width = getSize(data_dir / data_path)

                    # FIXME: after frontend shift to upperleft origion, simply remove below part
                    labels_temp = labels_d[label_fname]
                    for idx, label in enumerate(labels_temp):
                        temp = label["result"].split("|")
                        pidx = 0
                        while temp[pidx] != "":
                            temp[pidx] = f"{float(temp[pidx]) - ((width / 2) if pidx %2 ==0 else (height / 2)):.1f}"
                            pidx += 1
                        labels_temp[idx]["result"] = "|".join(temp)

                    self.add_task([{"path": str(data_path), "size": size}], [labels_temp], split=set_idx)
                    imported_data_path.add(data_path)
                    label_fnames.remove(label_fname)
                data_paths -= imported_data_path

        for data_path in data_paths:
            size, _, _ = getSize(data_dir / data_path)
            self.add_task([{"path": str(data_path), "size": size}], split=0)

        self.commit()

    def txt_exporter(self, export_dir: Path):
        project = self.project
        export_dir = Path(export_dir)

        # 2 export images
        tasks = Task._get(project_id=project.project_id, many=True)
        data_dir = export_dir / "image"
        create_dir(data_dir)
        data_info = {}
        sizes = {}

        for task in tasks:
            data = task.datas[0]
            sizes[data.data_id] = list(map(int, data.size.split(",")))[1:]
            copy(Path(project.data_dir) / data.path, data_dir)
            # data_info[data.data_id] = [task.set, Path(data.path).name.split(".")[0]]
            data_info[data.data_id] = [task.set, Path(data.path).name]

        # 3. export annotations
        annotations = Annotation._get(project_id=project.project_id, many=True)
        ann_dicts = [defaultdict(lambda: []), defaultdict(lambda: []), defaultdict(lambda: [])]
        for ann in annotations:
            r = ann.result.split("|")
            if r[0] == "no points":
                points = []
                r = r[2:]
            else:
                for ridx in range(len(r)):
                    if r[ridx] == "":
                        break
                ti = lambda v: int(float(v))
                points = [list(map(ti, vs)) for vs in zip(r[:ridx:2], r[1:ridx:2])]
                r = r[ridx + 1 :]
                print(sizes[ann.data_id])
                height, width = sizes[ann.data_id]
                for pidx in range(len(points)):
                    points[pidx][0] = int(points[pidx][0] + width / 2)
                    points[pidx][1] = int(points[pidx][1] + height / 2)

            split, name = data_info[ann.data_id]
            ann_dicts[split][name].append(
                {
                    "points": points,
                    "transcription": r[0],
                    "illegibility": bool(r[1]),
                    "language": r[2],
                }
            )
        names = ["train.txt", "val.txt", "test.txt"]
        for d, name in zip(ann_dicts, names):
            f = open(export_dir / name, "w")
            for k, v in d.items():
                print(f"{k}\t{json.dumps(v)}", file=f)
            f.close()
        """
        [
    {
        "transcription": "PHOCAPITAL",
        "points": [
            [
                67,
                51
            ],
            [
                327,
                46
            ],
            [
                327,
                74
            ],
            [
                68,
                80
            ]
        ],
        "difficult": false
    },
        """

    def json_importer(
        self,
        data_dir=None,
        filters={"exclude_prefix": ["."], "include_postfix": image_extensions},
    ):
        # ICDAR2019-LSVT-small

        # 1. set params
        project = self.project
        if data_dir is None:
            data_dir = project.data_dir
        data_dir = Path(data_dir)
        label_file_paths = ["train.json", "val.json", "test.json"]
        label_file_paths = [data_dir / f for f in label_file_paths]

        self.create_warning(data_dir)
        self.add_label(
            self.dummy_label_name,
            comment="Dummy label for ocr project, added for compatability, don't delete.",
            commit=True,
        )

        def _polygon_importer(data_paths, label_file_path, set=0):
            all_anns = json.loads(label_file_path.read_text(encoding="utf-8"))

            for file_name, anns in all_anns.items():
                img_paths = filter(lambda p: p.name == file_name or p.name.split(".")[0] == file_name, data_paths)
                img_paths = list(img_paths)
                if len(img_paths) != 1:
                    abort(
                        detail=f"{'No' if len(img_paths) == 0 else 'Multiple'} image(s) with path ending with {file_name} found under {data_dir}",
                        status=404,
                    )

                img_path = img_paths[0]
                data_paths.remove(img_path)
                size, _, _ = getSize(data_dir / img_path)

                """
                p1.w|p1.h|....|pn.w|pn.h|(固定为空，表示点结束)|transcription|illegibility(0/1)|language
                no points|(固定为空，表示点结束)|transcription|illegibility(0/1)|language

                full: {'transcription': '###', 'points': [[205, 367], [266, 382], [266, 389], [201, 372]], 'illegibility': True} 205|367|266|382|266|389|201|372||###|1
                no illegibility: {'transcription': '惠翎婚纱摄影', 'points': [[156, 331], [268, 365], [268, 382], [154, 360]]} 156|331|268|365|268|382|154|360||惠翎婚纱摄影|0
                no points: {'transcription': '鹊桥婚介所', 'illegibility': False} no points||鹊桥婚介所|0
                no transcription: {'points': [[103, 237], [583, 406], [583, 423], [108, 266]], 'illegibility': False} 103|237|583|406|583|423|108|266|||0
                """

                for idx, ann in enumerate(anns):
                    ann["frontend_id"] = idx + 1
                anns = list(map(self.encode_ann, anns))

                self.add_task([{"path": img_path, "size": size}], [anns], split=set)

            return data_paths

        # 2. find all images under data_dir
        data_paths = [Path(p) for p in listdir(data_dir, filters=filters)]
        for split_idx, label_file_path in enumerate(label_file_paths):
            if label_file_path.exists():
                data_paths = _polygon_importer(data_paths, label_file_path, split_idx)

        # 3. add tasks without label
        for data_path in data_paths:
            size, _, _ = getSize(data_dir / data_path)
            self.add_task([{"path": str(data_path), "size": size}])

        self.commit()

    def json_exporter(self, export_dir):
        # 1. set params
        project = self.project
        export_dir = Path(export_dir)

        # 2 export images
        tasks = Task._get(project_id=project.project_id, many=True)
        data_dir = export_dir / "image"
        create_dir(data_dir)
        data_info = {}
        for task in tasks:
            data = task.datas[0]
            copy(Path(project.data_dir) / data.path, data_dir)
            data_info[data.data_id] = [task.set, Path(data.path).name.split(".")[0]]

        # 3. export annotations
        annotations = Annotation._get(project_id=project.project_id, many=True)
        ann_dicts = [defaultdict(lambda: []), defaultdict(lambda: []), defaultdict(lambda: [])]
        for ann in annotations:
            r = ann.result.split("|")
            if r[0] == "no points":
                points = []
                r = r[2:]
            else:
                for idx in range(len(r)):
                    if r[idx] == "":
                        break
                ti = lambda v: int(float(v))
                points = [list(map(ti, vs)) for vs in zip(r[:idx:2], r[1:idx:2])]
                r = r[idx + 1 :]
            split, name = data_info[ann.data_id]
            ann_dicts[split][name].append(
                {
                    "points": points,
                    "transcription": r[0],
                    "illegibility": bool(r[1]),
                    "language": r[2],
                }
            )
        names = ["train.json", "val.json", "test.json"]
        for d, name in zip(ann_dicts, names):
            print(json.dumps(d), file=open(export_dir / name, "w"))
