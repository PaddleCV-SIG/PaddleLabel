import os.path as osp

# from connexion.resolver import RestyResolver

from pplabel import config, api
from pplabel.util import Resolver

connex_app = config.connex_app
connex_app.add_api(
    "openapi.yml",
    # resolver=RestyResolver("pplabel.api", collection_endpoint_name="get_all"),
    resolver=Resolver("pplabel.api", collection_endpoint_name="get_all"),
    strict_validation=True,  # request with undifiend keys return 400
)

if not osp.exists(config.sqlite_url):
    config.db.create_all()

def main():
    connex_app.run(port=5000, debug=True)


if __name__ == "__main__":
    main()
