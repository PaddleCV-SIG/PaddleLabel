import os
import argparse

from .serve import connexion_app


parser = argparse.ArgumentParser(description="PP Label")
parser.add_argument(
    "--lan",
    default=False,
    action="store_true",
    help="Whether to expose the service to lan",
)
parser.add_argument(
    "--port",
    default=17995,
    type=int,
    help="The port to use",
)
args = parser.parse_args()


def run():
    host = "0.0.0.0" if args.lan else "127.0.0.1"
    connexion_app.run(host=host, port=args.port, debug=True)


run()
