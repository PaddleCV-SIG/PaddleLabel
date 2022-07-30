import os.path as osp
import argparse

from tqdm import tqdm

from util.file import listdir, create_dir, copy

parser = argparse.ArgumentParser(
    description="Move single class classification images to class name folders based on xx_list.txt and labels.txt\n Note: only support consecutive label id"
)
parser.add_argument(
    "-i",
    "--dataset_path",
    type=str,
    required=True,
    help="Dataset path, should have labels.txt, and at least one of train_list.txt, val_list.txt and test_list.txt",
)
parser.add_argument("-o", "--output_path", type=str, required=True, help="The path to export dataset to")
parser.add_argument(
    "-id",
    "--input_delimiter",
    default=" ",
    type=str,
    help='Delimiter for input labels.txt, warped with "". For example " " for space or "|" for |. Defaults to space',
)

parser.add_argument(
    "-od",
    "--output_delimiter",
    default=" ",
    type=str,
    help="Delimiter for output labels.txt, same format as input_delimiter. Defaults to space",
)

args = parser.parse_args()

# 1. ensure essential files exist
labes_txt_path = osp.join(args.dataset_path, "labels.txt")
assert osp.exists(labes_txt_path), f"labels.txt not found under {args.dataset_path}"

xx_list_found = 0
list_paths = [osp.join(args.dataset_path, n) for n in ("train_list.txt", "val_list.txt", "test_list.txt")]
for list_path in list_paths:
    if osp.exists(list_path):
        xx_list_found += 1
assert xx_list_found != 0, f"No xx_list.txt found under {args.dataset_path}"

# 2. read info
all_files = set(listdir(args.dataset_path))

labels = open(labes_txt_path, "r").readlines()
labels = [l.strip() for l in labels]
labels = [l for l in labels if len(l) != 0]

idx2label = {}
for idx, name in enumerate(labels):
    idx2label[idx] = name

list_lines = []
for list_path in list_paths:
    if osp.exists(list_path):
        list_lines += open(list_path, "r").readlines()
list_lines = [l.strip() for l in list_lines]
list_lines = [l for l in list_lines if len(l) != 0]
list_info = [l.split(args.input_delimiter) for l in list_lines]

# 3. create output dirs and move files
for label_name in idx2label.values():
    create_dir(osp.join(args.output_path, label_name))

for img_path, label_id in tqdm(list_info):
    label_name = idx2label[int(label_id)]
    copy(osp.join(args.dataset_path, img_path), osp.join(args.output_path, label_name))
    all_files.remove(img_path)

# move all remaining files
for file in all_files:
    copy(osp.join(args.dataset_path, file), osp.join(args.output_path, file))
