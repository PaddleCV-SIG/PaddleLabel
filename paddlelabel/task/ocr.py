import os.path as osp
import json
from collections import defaultdict
from pathlib import Path

import cv2

from paddlelabel.task.util import create_dir, listdir, image_extensions
from paddlelabel.task.base import BaseTask
from paddlelabel.config import db
from paddlelabel.task.util.color import hex_to_rgb
from paddlelabel.task.util import copy
from paddlelabel.api.model import Task, Label, Annotation
from paddlelabel.api.util import abort
from paddlelabel.api.rpc.seg import polygon2points


class OpticalCharacterRecognition(BaseTask):
    def __init__(self, project, data_dir=None, is_export=False):
        super().__init__(project, skip_label_import=True, data_dir=data_dir, is_export=is_export)
        self.importers = {"polygon": self.polygon_importer}
        self.exporters = {"polygon": self.polygon_exporter}
        self.default_importer = self.polygon_importer
        self.default_exporter = self.polygon_exporter

    def polygon_importer(
        self,
        data_dir=None,
        filters={"exclude_prefix": ["."], "include_postfix": image_extensions},
    ):
        # 1. set params
        project = self.project
        if data_dir is None:
            data_dir = project.data_dir
        data_dir = Path(data_dir)
        label_file_paths = ["train.json", "val.json", "test.json"]
        label_file_paths = [data_dir / f for f in label_file_paths]

        self.create_warning(data_dir)
        label_name = "OCR Dummy Label"
        self.add_label(
            label_name,
            comment="Dummy label for ocr project, added for compatability, don't delete.",
            commit=True,
        )

        def _polygon_importer(data_paths, label_file_path, set=0):
            all_anns = json.loads(open(label_file_path, "r").read())

            for file_name, anns in all_anns.items():
                full_paths = filter(lambda p: p.name == file_name or p.name.split(".")[0] == file_name, data_paths)
                full_paths = list(full_paths)
                if len(full_paths) != 1:
                    abort(
                        detail=f"{'No' if len(full_paths) == 0 else 'Multiple'} image(s) with path ending with {file_name} found under {data_dir}",
                        status=404,
                    )

                full_path = full_paths[0]
                data_paths.remove(full_path)
                size = cv2.imread(osp.join(data_dir, full_path)).shape[:2]
                size = ",".join(map(str, size))

                """
                full: {'transcription': '###', 'points': [[205, 367], [266, 382], [266, 389], [201, 372]], 'illegibility': True} 205|367|266|382|266|389|201|372||###|1
                no illegibility: {'transcription': '惠翎婚纱摄影', 'points': [[156, 331], [268, 365], [268, 382], [154, 360]]} 156|331|268|365|268|382|154|360||惠翎婚纱摄影|0
                no points: {'transcription': '鹊桥婚介所', 'illegibility': False} no points||鹊桥婚介所|0
                no transcription: {'points': [[103, 237], [583, 406], [583, 423], [108, 266]], 'illegibility': False} 103|237|583|406|583|423|108|266|||0
                """

                def cvt_ann(ann):
                    res = ""
                    for p in ann.get("points", []):
                        res += "|".join(map(str, p)) + "|"
                    if len(res) == 0:
                        res += "no points|"
                    res += "|"
                    res += ann.get("transcription", "") + "|"
                    res += str(int(ann.get("illegibility", False))) + "|"
                    res += ann.get("language", "")
                    print(ann, res)
                    return {
                        "label_name": label_name,
                        "result": res,
                        "type": "ocr_polygon",
                        "frontend_id": ann["frontend_id"],
                    }

                for idx, ann in enumerate(anns):
                    ann["frontend_id"] = idx + 1
                anns = list(map(cvt_ann, anns))

                self.add_task([{"path": full_path, "size": size}], [anns], split=set)

            return data_paths

        # 2. find all images under data_dir
        data_paths = [Path(p) for p in listdir(data_dir, filters=filters)]
        for split_idx, label_file_path in enumerate(label_file_paths):
            if label_file_path.exists():
                data_paths = _polygon_importer(data_paths, label_file_path, split_idx)

        # 3. add tasks without label
        for data_path in data_paths:
            img = cv2.imread(str(data_dir / data_path))
            s = img.shape
            size = [1, s[1], s[0], s[2]]
            size = [str(s) for s in size]
            size = ",".join(size)
            self.add_task([{"path": data_path, "size": size}])

        db.session.commit()

    def polygon_exporter(self, export_dir):
        # 1. set params
        project = self.project
        export_dir = Path(export_dir)

        # 2.2 export images
        tasks = Task._get(project_id=project.project_id, many=True)
        data_dir = export_dir / "image"
        create_dir(data_dir)
        data_info = {}
        for task in tasks:
            data = task.datas[0]
            copy(Path(project.data_dir) / data.path, data_dir)
            data_info[data.data_id] = [task.set, Path(data.path).name.split(".")[0]]

        # 2.3 add annotations
        annotations = Annotation._get(project_id=project.project_id, many=True)
        ann_dicts = [defaultdict(lambda: []), defaultdict(lambda: []), defaultdict(lambda: [])]
        for ann in annotations:
            r = ann.result.split("|")
            # print(r)
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
            # {'transcription': '###', 'points': [[205, 367], [266, 382], [266, 389], [201, 372]], 'illegibility': True} 205|367|266|382|266|389|201|372|###|1
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

