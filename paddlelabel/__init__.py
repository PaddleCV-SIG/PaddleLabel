import pathlib
import logging

from sqlalchemy.engine import Engine
from sqlalchemy import event

print("Starting PaddleLabel")

HERE = pathlib.Path(__file__).parent
version = open((HERE / "version"), "r").read().strip()
# logger = logging.getLogger(__name__)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


from . import api, task
