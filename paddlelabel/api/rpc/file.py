import os
import os.path as osp

import connexion

from paddlelabel.config import data_base_dir
from paddlelabel.api.util import abort


def get_folders():
    path = connexion.request.json.get("path", None)
    if path is None:
        path = ""
    target = osp.join(data_base_dir, path)
    target = osp.abspath(target)
    # print(target, type(target))

    if not target[-1] == os.sep:
        target += os.sep
    if not target.startswith(osp.abspath(data_base_dir) + os.sep):
        abort("Can only request folders under data_base_dir", 500)
    if not osp.exists(target):
        return [], 200
    return next(os.walk(target))[1], 200
