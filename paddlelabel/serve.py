import os.path as osp
from importlib import resources
from pathlib import Path

from flask_cors import CORS
import flask

import paddlelabel
from paddlelabel.util import Resolver
from paddlelabel.config import sqlite_url, db, connexion_app, db_path
import paddlelabel.api
import paddlelabel.task


curr_dir = osp.abspath(osp.dirname(__file__))
HERE = Path(__file__).parent.absolute()


@connexion_app.app.route("/")
def index():
    return flask.redirect("/static/index.html")


if not osp.exists(db_path):
    print("Creating db")
    db.create_all()

    # TODO: move to base
    from paddlelabel.config import basedir
    from paddlelabel.api.controller.setting import init_site_settings

    # init_site_settings(resources.path("paddlelabel", "default_setting.json"))
    init_site_settings(HERE / "default_setting.json")


# yml_path = resources.path("paddlelabel", "openapi.yml")
# print(dir(yml_path))
connexion_app.add_api(
    # str(yml_path),
    osp.join(curr_dir, "openapi.yml"),
    resolver=Resolver("paddlelabel.api", collection_endpoint_name="get_all"),
    # request with undefined param returns error, dont enforce body
    strict_validation=True,
    pythonic_params=True,
)

CORS(connexion_app.app)
