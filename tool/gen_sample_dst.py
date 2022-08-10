import os.path as osp
import os

from file import listdir

paths = listdir(osp.join(osp.expanduser("~"), ".paddlelabel/sample/"))

paths = [p for p in paths if p[-len(".jpeg"):] == ".jpeg"]

for p in paths:
    print(f'"{p}"', end=",\n")