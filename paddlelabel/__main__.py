import os
import argparse
import logging

from .serve import connexion_app
from paddlelabel.api.controller.sample import prep_samples


def parse_args():
    parser = argparse.ArgumentParser(description="PP Label")
    parser.add_argument(
        "--lan",
        "-l",
        default=False,
        action="store_true",
        help="Whether to expose the service to lan",
    )
    parser.add_argument(
        "--port",
        "-p",
        default=17995,
        type=int,
        help="The port to use",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        default=False,
        action="store_true",
        help="Run quietly, when set, cmd will only output error",
    )
    parser.add_argument(
        "--debug",
        "-d",
        default=False,
        action="store_true",
        help="Run in debug mode",
    )

    return parser.parse_args()


def run():
    args = parse_args()

    prep_samples()

    host = "0.0.0.0" if args.lan else "127.0.0.1"

    logger = logging.getLogger("PaddleLabel")
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    formatter = logging.Formatter("[%(levelname)s]%(module)s.%(lineno)d: %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if args.quiet:
        logging.getLogger("werkzeug").setLevel(logging.ERROR)
        logging.getLogger("PaddleLabel").setLevel(logging.ERROR)

    if args.debug:
        logging.getLogger("werkzeug").setLevel(logging.INFO)
        logging.getLogger("PaddleLabel").setLevel(logging.DEBUG)

    logger.info("App starting")

    connexion_app.run(host=host, port=args.port, debug=args.debug)


run()
