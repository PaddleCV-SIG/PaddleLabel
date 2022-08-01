import argparse
import os.path as osp
import os

parser = argparse.ArgumentParser(description="Remove first value from labels.txt")
parser.add_argument(
    "-l", "--labels_path", type=str, required=True, help="Path to labels.txt. Use absolute path to be safe."
)
parser.add_argument(
    "-o",
    "--output_path",
    type=str,
    required=True,
    help="Path to output processed labels.txt. Use absolute path to be safe.",
)
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

if not osp.exists(args.labels_path):
    raise RuntimeError(f"Didn't find labels.txt at {args.labels_path}.")

lines = open(args.labels_path, "r").readlines()
lines = [l.strip() for l in lines if len(l.strip()) != 0]
lines = [l.split(args.input_delimiter) for l in lines]
lines = [l[1:] for l in lines]
lines = [args.output_delimiter.join(l) for l in lines]

os.makedirs(osp.dirname(args.output_path), exist_ok=True)
with open(args.output_path, "w") as f:
    for line in lines:
        print(line, file=f)
