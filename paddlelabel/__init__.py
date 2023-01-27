# -*- coding: utf-8 -*-
from __future__ import annotations
import logging

print("Starting PaddleLabel")

# 1. get version
from pathlib import Path

__version__ = open((Path(__file__).parent / "version"), "r").read().strip()


from dataclasses import dataclass

# 2. global configs
@dataclass
class Configs:
    host: str = "127.0.0.1"
    port: int = 17995
    debug: bool = False  # if running in debug mode
    log_level: int = logging.INFO

    # requests with the same request id arriving less than request_id_timeout s apart will be rejected
    request_id_timeout: float = 2

    """ file position settings """
    # _home: Path = Path(str(Path().home().absolute()).strip()) / ".paddlelabel"
    _home: Path = Path().home().absolute() / ".paddlelabel"
    install_base: Path = Path(__file__).absolute().parent  # TODO: a better name?

    @property
    def home(self) -> Path:
        return self._home

    @home.setter
    def home(self, home_path: Path | str):
        home_path = Path(home_path)
        if not home_path.exists():
            home_path.mkdir(parents=True)  # TODO: catch no permission
        self._home = home_path

    @property
    def sample_dir(self) -> Path:
        return self._home / "sample"

    # db settings
    db_engine: str = "sqlite"
    # db_head_version: str = "f47b7f5b73b9"  # latest db version
    SQLALCHEMY_ECHO: bool = False

    @property
    def db_path(self) -> Path:
        return self._home / "paddlelabel.db"

    @property
    def db_url(self) -> str:
        return f"{self.db_engine}:///{str(self.db_path)}"


configs = Configs()

# 3. enable foreign key constraint for sqlite
# TODO: run this conditionally based on db engine used
from sqlalchemy.engine import Engine
from sqlalchemy import event


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
