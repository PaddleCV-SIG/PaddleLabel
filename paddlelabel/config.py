# -*- coding: utf-8 -*-
# TODO: move all functions in this file to serve.py
from pathlib import Path
import logging

import connexion
from flask_sqlalchemy import SQLAlchemy  # TODO: remove
from flask_marshmallow import Marshmallow  # TODO: remove

from paddlelabel.util import rand_string
from paddlelabel import configs

HERE = Path(__file__).parent.absolute()
logger = logging.getLogger("paddlelabel")

# if not configs.db_path.parent.exists():
#     configs.db_path.parent.mkdir()

logger.info(f"Database path: {configs.db_url}")

connexion_app = connexion.App("PaddleLabel")
app = connexion_app.app
app.config["SQLALCHEMY_DATABASE_URI"] = configs.db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = configs.SQLALCHEMY_ECHO
app.config["SECRET_KEY"] = rand_string(30)

app.static_url_path = "/static"
app.static_folder = str((HERE / "static").absolute())

db = SQLAlchemy(app)
se = db.session
ma = Marshmallow(app)
