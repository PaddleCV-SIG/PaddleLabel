import os
import os.path as osp
from pathlib import Path

import connexion
from flask_sqlalchemy import SQLAlchemy  # TODO: remove
from flask_marshmallow import Marshmallow  # TODO: remove
from flask_cors import CORS

from paddlelabel.util import rand_string


basedir = osp.abspath(osp.dirname(__file__))

# db_path = f"{osp.join(os.path.expanduser('~'), '.paddlelabel', 'paddlelabel.db')}"  # TODO: make this Path
db_path = Path.home() / ".paddlelabel" / "paddlelabel.db"  # TODO: make this Path
db_path = str(db_path)

if not osp.exists(osp.dirname(db_path)):
    os.makedirs(osp.dirname(db_path))
db_url = f"sqlite:///{db_path}"
print(f"Database path: {db_url}".encode("utf-8"))

connexion_app = connexion.App("PaddleLabel")
app = connexion_app.app
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["SECRET_KEY"] = rand_string(30)

app.static_url_path = "/static"
app.static_folder = osp.join(basedir, "static")
CORS(connexion_app.app)

db = SQLAlchemy(app)
se = db.session
ma = Marshmallow(app)
db_head_version = "f47b7f5b73b9"

# reject requests with the same request_id within request_id_timeout seconds
request_id_timeout = 2

data_base_dir = osp.join(os.path.expanduser("~"), ".paddlelabel")  # TODO: make this Path
