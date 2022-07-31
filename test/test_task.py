import os.path as osp

import paddlelabel
from paddlelabel.config import sqlite_url, db

if not osp.exists(sqlite_url):
    print("Creating db")
    db.create_all()

    # TODO: move to base
    from paddlelabel.config import basedir
    from paddlelabel.api.controller.setting import init_site_settings

    init_site_settings(osp.join(basedir, "default_setting.json"))

# paddlelabel.task.classification.test()

paddlelabel.task.classification.single_clas()
# paddlelabel.task.classification.multi_clas()
#
# paddlelabel.task.detection.voc()
# paddlelabel.task.detection.coco()
