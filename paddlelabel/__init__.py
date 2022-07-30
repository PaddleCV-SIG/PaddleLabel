import pathlib

from sqlalchemy.engine import Engine
from sqlalchemy import event

HERE = pathlib.Path(__file__).parent

version = open((HERE / "version"), "r").read().strip()


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


from . import api, task
