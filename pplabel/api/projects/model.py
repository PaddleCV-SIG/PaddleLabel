from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import Column

from pplabel.config import db
from pplabel.api.util import nncol


class Project(db.Model):
    __tablename__ = "project"
    __table_args__ = {"comment": "Contains all the project information and settings"}
    project_id = nncol(
        sa.Integer,
        primary_key=True,
    )
    name = nncol(sa.String())
    description = Column(sa.String())
    category = nncol(sa.SmallInteger())
    data_dir = nncol(sa.String())
    label_dir = nncol(sa.String())
    label_config = Column(sa.String())
    created = nncol(sa.DateTime, default=datetime.utcnow)
    modified = nncol(sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    other_settings = Column(sa.String())
