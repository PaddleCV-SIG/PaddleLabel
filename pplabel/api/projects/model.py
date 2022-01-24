from datetime import datetime

import sqlalchemy as sa

from pplabel.config import db

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
    project_id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(
        sa.String(), nullable=False
    )  # TODO: chinese string, constraint by bytes

    # description = sa.Column(sa.String(32))
    # category = sa.Column(sa.Integer)
    # data_dir = sa.Column(sa.String(32))
    # label_dir = sa.Column(sa.String(32))
    # modified = sa.Column(sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # created = sa.Column(sa.DateTime, default=datetime.utcnow)
