import os.path as osp

# from swagger_ui_bundle import swagger_ui_3_path

from pplabel import config, api
from pplabel.util import Resolver

# print(swagger_ui_3_path)
# options = {"swagger_path": swagger_ui_3_path}
connex_app = config.connex_app
connex_app.add_api(
    "openapi.yml",
    # resolver=RestyResolver("pplabel.api", collection_endpoint_name="get_all"),
    resolver=Resolver("pplabel.api", collection_endpoint_name="get_all"),
    # request with undefined param returns error, not enforced in request body
    strict_validation=True,
    pythonic_params=True
    # options=options,
)

if not osp.exists(config.sqlite_url):
    config.db.create_all()


def main():
    connex_app.run(port=5000, debug=True)


if __name__ == "__main__":
    main()
