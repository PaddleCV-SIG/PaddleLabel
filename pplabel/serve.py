import os.path as osp
import traceback

from .util import Resolver

import os
import os.path as osp
import random
import string


# TODO: take config out
### config ###
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from .util import rand_string

# from pplabel.serve import api
basedir = os.path.abspath(os.path.dirname(__file__))

sqlite_url = "sqlite:///" + osp.normcase(osp.join(basedir, "pplabel.db"))

connexion_app = connexion.App(__name__)
app = connexion_app.app
app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.secret_key = rand_string(20)

db = SQLAlchemy(app)
se = db.session
ma = Marshmallow(app)
###

request_id_timeout = 2  # reject requests with the same request_id within 2 seconds

connexion_app.add_api(
    "openapi.yml",
    resolver=Resolver("pplabel.api", collection_endpoint_name="get_all"),
    # request with undefined param returns error, dont enforce body
    strict_validation=True,
    pythonic_params=True,
)


for line in traceback.format_stack():
    print(line.strip())

if not osp.exists(sqlite_url):
    db.create_all()
    from . import api

    api.setting.init_site_settings(
        osp.normpath(osp.join(basedir, "default_setting.json"))
    )

# TODO: add https support
# config.connexion_app.run(port=5000)
