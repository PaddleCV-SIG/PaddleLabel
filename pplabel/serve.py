import os
import os.path as osp
import logging

import pplabel
from pplabel.util import Resolver
from pplabel.config import sqlite_url, db, connexion_app
import pplabel.api
import pplabel.task

logging.getLogger("pplabel").debug("in server.py")

if not osp.exists(sqlite_url):
    print("Creating db")
    db.create_all()

    # TODO: move to base
    from pplabel.config import basedir
    from pplabel.api.controller.setting import init_site_settings

    init_site_settings(osp.normpath(osp.join(basedir, "default_setting.json")))


connexion_app.add_api(
    "openapi.yml",
    resolver=Resolver("pplabel.api", collection_endpoint_name="get_all"),
    # request with undefined param returns error, dont enforce body
    strict_validation=True,
    pythonic_params=True,
)
