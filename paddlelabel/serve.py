# -*- coding: utf-8 -*-
from pathlib import Path
import shutil
import logging

from flask_cors import CORS  # TODO: custom middleware, dont use this package
import alembic
from alembic.config import Config
from alembic.script import ScriptDirectory

from paddlelabel import configs
from paddlelabel.util import Resolver, backend_error
from paddlelabel.config import connexion_app
from paddlelabel.api.controller.setting import init_site_settings
from paddlelabel.api.model import AlembicVersion

HERE = Path(__file__).parent.absolute()
logger = logging.getLogger("paddlelabel")

# 1. static routes
@connexion_app.app.route("/")
def index():
    return "", 301, {"Location": "/static/index.html"}


@connexion_app.app.route("/static/doc/")
def doc_index():
    return "", 301, {"Location": "/static/doc/index.html"}


@connexion_app.app.route("/static/doc/CN/")
def cn_doc_index():
    return "", 301, {"Location": "/static/doc/CN/index.html"}


@connexion_app.app.route("/static/doc/EN/")
def en_doc_index():
    return "", 301, {"Location": "/static/doc/EN/index.html"}


# 2. update db version
db_exists = configs.db_path.exists()
alembic_cfg = alembic.config.Config(HERE / "alembic.ini")
alembic_cfg.set_main_option("script_location", str(HERE / "dbmigration"))
alembic_cfg.set_main_option("sqlalchemy.url", configs.db_url)
# Create the alembic version table if it doesn’t exist already
alembic.command.ensure_version(alembic_cfg)

with connexion_app.app.app_context():
    res = AlembicVersion.query.all()
    # get version in db
    curr_db_v = None if len(res) == 0 else res[0].version_num
    # get version of revision head
    script = ScriptDirectory.from_config(alembic_cfg)
    heads = script.get_revisions("heads")
    db_head_version = heads[0].revision

    # v0.1.0: db exists but doesn't have version
    if curr_db_v is None and db_exists:
        alembic.command.stamp(alembic_cfg, revision="23c1bf9b7f48")

    # need db backup
    if curr_db_v != db_head_version and db_exists:
        from datetime import datetime

        back_up_path = (
            Path(configs.db_path).parent
            / f"{str(datetime.now()).split('.')[0].replace(' ', '_').replace(':', '_')}-paddlelabel.db.bk"
        )
        shutil.copy(Path(configs.db_path), back_up_path)
        logger.warn(
            f"Performing database update. Should anything goes wrong during this update, you can find the old database at {str(back_up_path)}"
        )

    # perform db upgrade
    alembic.command.upgrade(alembic_cfg, "head")

    # TODO:  move this to be managed by alembic @lin
    init_site_settings(HERE / "default_setting.json")

    if configs.debug:
        alembic.command.check(alembic_cfg)  # abort when model definition is changed and a new reversion is required

logger.setLevel(configs.log_level)

# 3. serve the app
connexion_app.add_api(
    HERE / "openapi.yml",
    resolver=Resolver("paddlelabel.api", collection_endpoint_name="get_all"),
    # request with undefined param returns error, dont enforce body
    strict_validation=True,
    pythonic_params=True,
    options={"swagger_ui": configs.debug},
)
connexion_app.add_error_handler(Exception, backend_error)

# TODO: use middleware, instead of flask-cors
CORS(connexion_app.app)
