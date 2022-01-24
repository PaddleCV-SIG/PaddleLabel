from datetime import datetime

import sqlalchemy as sa

from pplabel.config import db


class Task(db.Model):
    __tablename__ = "task"
    task_id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(
        sa.String(), nullable=False
    )  # TODO: chinese string, constraint by bytes

    # description = sa.Column(sa.String(32))
    # category = sa.Column(sa.Integer)
    # data_dir = sa.Column(sa.String(32))
    # label_dir = sa.Column(sa.String(32))
    # modified = sa.Column(sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # created = sa.Column(sa.DateTime, default=datetime.utcnow)
