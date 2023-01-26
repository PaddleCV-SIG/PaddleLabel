# -*- coding: utf-8 -*-
import argparse
import logging
import logging.config
import webbrowser
from pathlib import Path
import logging

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
    # TODO: test implement

    return parser.parse_args()


def run():
    args = parse_args()

    # 1. pre run checks and setup
    # 1.1 configure logger
    logging.config.fileConfig(fname=HERE / "alembic.ini", disable_existing_loggers=False)
    logger = logging.getLogger("paddlelabel")
    if args.debug:
        levels = (logging.WARNING, logging.DEBUG)
    elif args.verbose:
        levels = (logging.INFO, logging.DEBUG)
    else:
        levels = (logging.WARNING, logging.INFO)
    logging.getLogger("werkzeug").setLevel(levels[0])
    logger.setLevel(levels[1])
    configs.log_level = levels[1]

    from paddlelabel.util import pyVerGt, portInUse, can_update

    # 1.2 ensure port not in use
    if not args.debug and portInUse(args.port):  # port will be in use with cypress open
        logging.error(
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

    # 2.1 set configs
    configs.host = "0.0.0.0" if args.lan else "127.0.0.1"
    configs.port = args.port
    configs.debug = args.debug
    configs.home = args.home

    # 2.2 import
    from paddlelabel import api, task
    from paddlelabel.api.controller.sample import prep_samples
    from paddlelabel.serve import connexion_app

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
