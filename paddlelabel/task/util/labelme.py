# -*- coding: utf-8 -*-
from pathlib import Path
import json
import logging
import os.path as osp

from .file import rget_by_ext

logger = logging.getLogger("paddlelabel")


class LabelMe:
    def __init__(self, data_dir: Path, ann_file_endings: list[str] = [".json"]):
        """
        1. match by train/val/test_list.txt
        2. match by json content
        3. match by json content same base filename
        4. match by json and image file same base filename
        """

        # determined matchings, {img_path: (ann_path | None, set_idx)}
        matchings: dict[Path, tuple[Path | None, int]] = {}

        ann_paths = set(rget_by_ext(data_dir, ann_file_endings))
        img_paths = set(rget_by_ext(data_dir))

        # 1. get matching info from list files
        list_files = {"train_list.txt": 0, "val_list.txt": 1, "test_list.txt": 2}

        for list_file, set_idx in list_files.items():
            list_file = data_dir / list_file
            if not list_file.exists():
                continue

            for line_idx, line in enumerate(list_file.read_text(encoding="utf8").split("\n")):
                line = line.strip()
                if line == "":
                    continue
                # TODO: try catch this split, import only set not ann path
                img_path, ann_path = map(lambda p: Path(osp.normpath(data_dir / p)), line.split(" "))

                assert (
                    img_path in img_paths
                ), f"Image file {str(img_path)} listed at line {line_idx} in {str(list_file)} not found on disk"
                assert (
                    ann_path in ann_paths
                ), f"Annotation file {str(ann_path)} listed at line {line_idx} in {str(list_file)} not found on disk"

                matchings[img_path] = (ann_path, set_idx)

                img_paths.remove(img_path)
                ann_paths.remove(ann_path)

        logger.debug(f"list matchings: {len(matchings)} {matchings}")

        # 2. get match from json ann content
        ann2img_path = {f: self.ann_path2img_path(f) for f in ann_paths}
        for ann_path, img_path in list(ann2img_path.items()):
            if img_path in img_paths:
                matchings[img_path] = (ann_path, 0)

                ann_paths.remove(ann_path)
                img_paths.remove(img_path)
                del ann2img_path[ann_path]

        logger.debug(f"json content matching: {len(matchings)} {matchings}")

        # 3. match by json content has same base filename as img file
        img_base_names = {p.name.split(".")[0]: p for p in img_paths}
        for ann_path, img_path in list(ann2img_path.items()):
            base_name = img_path.name.split(".")[0]
            if base_name in img_base_names:
                img_path = img_base_names[base_name]
                matchings[img_path] = (ann_path, 0)

                ann_paths.remove(ann_path)
                img_paths.remove(img_path)
                del img_base_names[base_name]
                del ann2img_path[ann_path]

        logger.debug(f"json content same base name matching: {len(matchings)} {matchings}")

        ann_base_names = {p.name.split(".")[0]: p for p in ann_paths}

        for base_name in ann_base_names:
            if base_name in img_base_names:
                img_path = img_base_names[base_name]
                ann_path = ann_base_names[base_name]
                matchings[img_path] = (ann_path, 0)

                ann_paths.remove(ann_path)
                img_paths.remove(img_path)
                # NOTE: if need two mappings later, keep values up to date
                # del img_base_names[base_name]
                # del ann_base_names[base_name]

        for img_path in img_paths:
            matchings[img_path] = (None, 0)

        self.matchings = matchings

        # for m in matchings.items():
        #     print(m)

        # 1 / 0

    def ann_path2img_path(self, ann_path: Path) -> Path:
        """
        Parse image path from annotation file

        Parameters
        ----------
        ann_path : Path
            Path to annotation file

        Returns
        -------
        Path
            **Resolved** path to image file, parsed from annotation file content
        """
        img_path = ann_path.parent / json.loads(ann_path.read_text(encoding="utf8"))["imagePath"]
        return Path(osp.normpath(img_path))

    def parse_ann(self, ann_path: Path, ann_types: set[str]):
        assert ann_path.exists(), f"Ann path specified {str(ann_path)} doesn't exist"
        info = json.loads(ann_path.read_text(encoding="utf8"))
        height, width = info["imageHeight"], info["imageWidth"]

        shapes = info["shapes"]
        anns = []

        for shape in shapes:
            if shape["shape_type"] in ann_types:
                if shape["shape_type"] == "point":
                    # result: "x,y" (h pos, v pos), integers
                    anns.append(
                        {
                            "label_name": shape["label"],
                            "result": ",".join(map(lambda v: str(int(float(v))), shape["points"][0])),
                            "frontend_id": len(anns) + 1,
                            "type": "point",
                        }
                    )
        return height, width, anns
