import os
import os.path as osp

import connexion
from flask_sqlalchemy import SQLAlchemy  # TODO: remove
from flask_marshmallow import Marshmallow  # TODO: remove
from flask_cors import CORS

from .util import rand_string

basedir = os.path.abspath(os.path.dirname(__file__))

db_path = f"{osp.join(os.path.expanduser('~'), '.paddlelabel', 'paddlelabel.db')}"

if not osp.exists(osp.dirname(db_path)):
    os.makedirs(osp.dirname(db_path))
sqlite_url = f"sqlite:///{db_path}"
print("database url: ", sqlite_url)

connexion_app = connexion.App(__name__)
app = connexion_app.app
app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["SECRET_KEY"] = rand_string(30)
app.static_url_path = "/static"
app.static_folder = osp.join(basedir, "static")
CORS(connexion_app.app)

db = SQLAlchemy(app)
se = db.session
ma = Marshmallow(app)


# reject requests with the same request_id within request_id_timeout seconds
request_id_timeout = 2

data_base_dir = osp.join(os.path.expanduser("~"), ".paddlelabel")
