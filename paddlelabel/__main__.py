import os
import argparse
import logging

from paddlelabel.serve import connexion_app
from paddlelabel.api.controller.sample import prep_samples
from paddlelabel.util import pyVerGt, portInUse


def parse_args():
    parser = argparse.ArgumentParser(description="PP Label")
    parser.add_argument(
        "--lan",
        "-l",
        default=False,
        action="store_true",
        help="Whether to expose PaddleLabel to lan",
    )
    parser.add_argument(
        "--port",
        "-p",
        default=17995,
        type=int,
        help="The port to use",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        default=False,
        action="store_true",
        help="Output more log in command line, if not set, cmd will only output error",
    )
    parser.add_argument(
        "--debug",
        "-d",
        default=False,
        action="store_true",
        help="Run in debug mode",
    )

    return parser.parse_args()


pyVerWarning = """
It's recommended to run PaddleLabel with Python>=3.9.0. Please consider creating a new virtual enviroment and run PaddleLabel with:

conda create -y -n paddlelabel python=3.9
conda activate paddlelabel
pip install --upgrade paddlelabel
paddlelabel

"""


def run():
    args = parse_args()

    # 1. ensuer port not in use
    if portInUse(args.port):
        print(
            f"Port {args.port} is currently in use. Please identify and stop that process using port {args.port} or specify a different port with: paddlelabel -p [Port other than {args.port}]."
        )
        exit()

    # 2. warn if low py version
    if not pyVerGt():
        print(pyVerWarning)

    # 3. create sample datasets
    prep_samples()

    host = "0.0.0.0" if args.lan else "127.0.0.1"

    logger = logging.getLogger("PaddleLabel")
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    formatter = logging.Formatter("[%(levelname)s]%(module)s.%(lineno)d: %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    logging.getLogger("PaddleLabel").setLevel(logging.ERROR)

    if args.debug or args.verbose:
        logging.getLogger("werkzeug").setLevel(logging.INFO)
        logging.getLogger("PaddleLabel").setLevel(logging.DEBUG)

    logger.info("App starting")
    print(f"PaddleLabel is running at http://localhost:{args.port}")
    connexion_app.run(host=host, port=args.port, debug=args.debug)


run()
