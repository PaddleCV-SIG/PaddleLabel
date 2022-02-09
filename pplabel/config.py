import os
import os.path as osp
import logging

import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from .util import rand_string

logging.basicConfig(
    level=logging.ERROR,
    filename="pplabel.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
)
logging.getLogger("pplabel").setLevel(logging.DEBUG)

basedir = os.path.abspath(os.path.dirname(__file__))

# sqlite_url = "sqlite:///" + osp.normcase(osp.join(basedir, "pplabel.db"))
sqlite_url = f"sqlite:///{osp.join(os.path.expanduser('~'), '.pplabel/pplabel.db')}"

connexion_app = connexion.App(__name__)
app = connexion_app.app
app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_ECHO"] = True
app.secret_key = rand_string(20)

db = SQLAlchemy(app)
se = db.session
ma = Marshmallow(app)

request_id_timeout = (
    2  # reject requests with the same request_id within request_id_timeout seconds
)

task_test_basedir = "/home/lin/Desktop/data/pplabel/demo"
