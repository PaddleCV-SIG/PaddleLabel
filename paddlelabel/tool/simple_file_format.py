# -*- coding: utf-8 -*-
from pathlib import Path


def eiseg_label2_paddlelabel(eiseg_label_path: Path, add_background: bool = False, label_id_delta: int = 0):
    # 1. read eiseg label
    eiseg_label = eiseg_label_path.read_text(encoding="utf-8").split("\n")
    eiseg_label = [l.split(" ") for l in eiseg_label if len(l) != 0]

    # 2.1 split
    pdlabel_label = [[l[1], l[0], *l[2:]] for l in eiseg_label]
    # # 2.2 change label id
    if label_id_delta != 0:
        for idx in range(len(pdlabel_label)):
            pdlabel_label[idx][1] = str(int(pdlabel_label[idx][1]) + label_id_delta)
    # 2.3 join to string
    pdlabel_label = [" ".join(l) for l in pdlabel_label]
    # 2.4 add background line
    pdlabel_label = ["background 0 0 0 0"] + pdlabel_label if add_background else pdlabel_label
    # 2.5 join to file
    pdlabel_label = "\n".join(pdlabel_label)

    # 3. rename eiseg format file and write pdlabel format file
    orig_name = eiseg_label_path.name
    name, ext = orig_name.split(".")
    eiseg_label_path.rename(eiseg_label_path.parent / f"{name}_eiseg.{ext}")
    pdlabel_label_path = eiseg_label_path.parent / orig_name
    pdlabel_label_path.write_text(pdlabel_label)
