import argparse
import logging
import webbrowser
from pathlib import Path

import paddlelabel
from paddlelabel.serve import connexion_app
from paddlelabel.api.controller.sample import prep_samples
from paddlelabel.util import pyVerGt, portInUse

HERE = Path(__file__).parent.absolute()


def parse_args():
    parser = argparse.ArgumentParser(description="PaddleLabel")
    parser.add_argument(
        "--lan",
        "-l",
        default=False,
        action="store_true",
        help="Expose PaddleLabel service to lan",
    )
    parser.add_argument(
        "--port",
        "-p",
        default=17995,
        type=int,
        help="The port PaddleLabel will run on",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        default=False,
        action="store_true",
        help="Output more log in command line. If not set, defaults to output only warning and error logs",
    )
    parser.add_argument(
        "--debug",
        "-d",
        default=False,
        action="store_true",
        help="Run in debug mode, will restart PaddleLabel on code save",
    )

    return parser.parse_args()


pyVerWarning = """
It's recommended to run PaddleLabel with Python>=3.9.0. Please consider running PaddleLabel in a new virtual environment with:

conda create -y -n paddlelabel python=3.11
conda activate paddlelabel
pip install --upgrade paddlelabel
paddlelabel

"""


def run():
    args = parse_args()

    # 1. ensure port not in use
    if not args.debug and not args.verbose and portInUse(args.port):
        print(
            f"Port {args.port} is currently in use. Please identify and stop that process using port {args.port} or specify a different port with: paddlelabel -p [Port other than {args.port}]."
        )
        exit()

    # 2. warn if low py version
    if not pyVerGt():
        print(pyVerWarning)

    host = "0.0.0.0" if args.lan else "127.0.0.1"

    # 3. configure logger and logging levels
    logger = logging.getLogger("paddlelabel")
    logger.propagate = False
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)s [paddlelabel.%(module)s.%(lineno)d]: %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if args.debug:
        logging.getLogger("werkzeug").setLevel(logging.WARNING)
        logger.setLevel(logging.DEBUG)
    elif args.verbose:
        logging.getLogger("werkzeug").setLevel(logging.INFO)
        logger.setLevel(logging.DEBUG)
    else:
        logging.getLogger("werkzeug").setLevel(logging.WARNING)
        logger.setLevel(logging.INFO)

    logger.info(f"Version: {paddlelabel.version}")
    # logger.debug("debug")
    # logger.critical("ceritical")

    # 4. run
    if not args.debug:
        webbrowser.open(f"http://localhost:{args.port}")

    # 5. create sample datasets
    prep_samples()

    print(f"PaddleLabel is running at http://localhost:{args.port}")
    connexion_app.run(host=host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    run()
