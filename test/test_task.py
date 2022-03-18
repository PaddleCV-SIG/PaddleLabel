import os.path as osp

import pplabel
from pplabel.config import sqlite_url, db

if not osp.exists(sqlite_url):
    print("Creating db")
    db.create_all()

    # TODO: move to base
    from pplabel.config import basedir
    from pplabel.api.controller.setting import init_site_settings

    init_site_settings(osp.normpath(osp.join(basedir, "default_setting.json")))

# pplabel.task.classification.test()

pplabel.task.classification.single_clas()
# pplabel.task.classification.multi_clas()
#
# pplabel.task.detection.voc()
# pplabel.task.detection.coco()
