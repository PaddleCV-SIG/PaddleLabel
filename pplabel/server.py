import os.path as osp

from flask import render_template
from connexion.resolver import RestyResolver

# Local modules
from pplabel import config, api

# Get the application instance
connex_app = config.connex_app
# print(osp.join(config.basedir, "openapi.yaml"))

connex_app.add_api(
    "openapi.yml",
    resolver=RestyResolver("pplabel.api"),
    strict_validation=True,  # request with undifiend keys return 400
)

if not osp.exists(config.sqlite_url):
    config.db.create_all()


def main():
    connex_app.run(port=5000, debug=True)


if __name__ == "__main__":
    main()
