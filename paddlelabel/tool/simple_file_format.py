from pathlib import Path


def eiseg_label2_paddlelabel(eiseg_label_path: Path):
    eiseg_label = eiseg_label_path.read_text(encoding="utf-8").split("\n")
    eiseg_label = [l.split(" ") for l in eiseg_label if len(l) != 0]
    pdlabel_label = "\n".join(["background 0 0 0 0"] + [" ".join([l[1], l[0], *l[2:]]) for l in eiseg_label])
    orig_name = eiseg_label_path.name
    name, ext = orig_name.split(".")
    eiseg_label_path.rename(eiseg_label_path.parent / f"{name}_eiseg.{ext}")
    pdlabel_label_path = eiseg_label_path.parent / orig_name
    pdlabel_label_path.write_text(pdlabel_label)
