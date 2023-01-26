# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path

from PIL import Image


def getSize(img_path: Path) -> tuple[str, int, int]:
    im = Image.open(img_path)
    width, height = im.size
    s = ",".join(map(str, (1,) + (height, width)))
    return s, height, width
