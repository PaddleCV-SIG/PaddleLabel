from pathlib import Path

# import logging

import connexion
from flask_sqlalchemy import SQLAlchemy  # TODO: remove
from flask_marshmallow import Marshmallow  # TODO: remove
from flask_cors import CORS

from paddlelabel.util import rand_string
from paddlelabel import configs

# logger = logging.getLogger("paddlelabel")

# basedir = Path(__file__).parent.absolute()  # TODO: remove
HERE = Path(__file__).parent.absolute()

if not configs.db_path.parent.exists():
    configs.db_path.parent.mkdir()

# logger.info(f"Database path: {configs.db_url}")

connexion_app = connexion.App("PaddleLabel")
app = connexion_app.app
app.config["SQLALCHEMY_DATABASE_URI"] = configs.db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = configs.SQLALCHEMY_ECHO
app.config["SECRET_KEY"] = rand_string(30)

app.static_url_path = "/static"
app.static_folder = str((HERE / "static").absolute())
CORS(connexion_app.app)

db = SQLAlchemy(app)
se = db.session
ma = Marshmallow(app)

# reject requests with the same request_id within request_id_timeout seconds
request_id_timeout = 2

# data_base_dir = osp.join(os.path.expanduser("~"), ".paddlelabel")  # TODO: make this Path
