import os
import os.path as osp
import random
import string

import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import session, request

from pplabel.util import rand_string

basedir = os.path.abspath(os.path.dirname(__file__))

connex_app = connexion.App(__name__)
app = connex_app.app

sqlite_url = "sqlite:///" + os.path.join(basedir, "pplabel.db")

app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)
se = db.session
ma = Marshmallow(app)

request_id_timeout = 2

app.secret_key = rand_string(20)
