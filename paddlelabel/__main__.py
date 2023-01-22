import argparse
import logging
import webbrowser
from pathlib import Path

from paddlelabel import __version__, configs

HERE = Path(__file__).parent.absolute()


def parse_args():
    parser = argparse.ArgumentParser(description="PaddleLabel")
    parser.add_argument(
        "--lan",
        "-l",
        default=False,
        action="store_true",
        help="Expose PaddleLabel service to lan. Defaults to False",
    )
    parser.add_argument(
        "--port",
        "-p",
        default=17995,
        type=int,
        help="The port PaddleLabel will run on. Defaults to 17995",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        default=False,
        action="store_true",
        help="Output more log from web server. Defaults to only show web server error",
    )
    parser.add_argument(
        "--debug",
        "-d",
        default=False,
        action="store_true",
        help="Run in debug mode, will restart PaddleLabel on code is saved, output debug log and skip opening browser. Defaults to False",
    )
    home = configs.home
    parser.add_argument(
        "--home",
        type=str,
        default=home,
        help=f"The folder to store paddlelabel files, like database and built in samples. Defaults to {home}",
    )
    # TODO:  implement

    return parser.parse_args()


def run():
    args = parse_args()

    # 1. pre run checks and setup
    # 1.1 configure logger
    logger = logging.getLogger("paddlelabel")
    logger.propagate = False
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)s [paddlelabel.%(module)s.%(lineno)d]: %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if args.debug:
        levels = (logging.WARNING, logging.DEBUG)
    elif args.verbose:
        levels = (logging.INFO, logging.DEBUG)
    else:
        levels = (logging.WARNING, logging.INFO)

    logging.getLogger("werkzeug").setLevel(levels[0])
    logger.setLevel(levels[1])
    for handler in logger.handlers:
        handler.setLevel(levels[1])

    from paddlelabel.util import pyVerGt, portInUse, can_update

    # 1.2 ensure port not in use
    if not args.debug and not args.verbose and portInUse(args.port):
        print(
            f"Port {args.port} is currently in use. Please identify and stop that process using port {args.port} or specify a different port with: paddlelabel -p [Port other than {args.port}]."
        )
        exit()

    # 1.3 warn if low py version
    pyVerWarning = """
It's recommended to run PaddleLabel with Python>=3.9.0. Please consider running PaddleLabel in a new virtual environment with:

conda create -y -n paddlelabel python=3.11
conda activate paddlelabel
pip install --upgrade paddlelabel
paddlelabel

"""
    if not pyVerGt(version="3.9.0"):
        print(pyVerWarning)

    # 1.4 check for updates
    can_update(log=True)

    # 2. prepare and start

    # 2.1 import
    from paddlelabel import api, task
    from paddlelabel.serve import connexion_app
    from paddlelabel.api.controller.sample import prep_samples

    # 2.2 configs
    configs.host = "0.0.0.0" if args.lan else "127.0.0.1"
    configs.port = args.port
    configs.debug = args.debug
    configs.home = args.home

    # 2.3 create sample projects
    prep_samples()

    # 2.4 fire up browser
    if not configs.debug:
        webbrowser.open(f"http://localhost:{configs.port}")

    # 2.5 serve app
    logger.info(f"Version: {__version__}")
    logger.info(f"PaddleLabel is running at http://localhost:{configs.port}")

    connexion_app.run(host=configs.host, port=configs.port, debug=configs.debug)


if __name__ == "__main__":
    run()
