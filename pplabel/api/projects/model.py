from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import Column

from pplabel.config import db
from pplabel.api.util import nncol

"""
- Project
  - Project id
  - Project name
  - Project description
  - Project category : a number indicating top project category
  - Data dir : directory storing datas
  - Label dir : directory storing labels
  - Label config: json, specific to each annotation type
  - Date created
  - Other project specific settings: json
    - Segmentation
      - annotation format : mask/polygon
      - brush size
    - Keypoint
      - Keypoint number
"""


class Project(db.Model):
    __tablename__ = "project"
    project_id = nncol(sa.Integer, primary_key=True)
    name = nncol(sa.String())
    description = Column(sa.String())
    category = nncol(sa.SmallInteger())
    data_dir = nncol(sa.String())
    label_dir = nncol(sa.String())
    # label_config =
    created = nncol(sa.DateTime, default=datetime.utcnow)
    modified = nncol(sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
