from datetime import datetime

from pplabel.config import db
from pplabel.api.util import nncol

"""
- Task: an annotation task, links data and annotation
  - Task id : unique across all tasks (even tasks under different projects wont have the same task id)
  - Project id : the project this task belongs to
  - Data : a relative path from project data dir. Can be a file or a directory.
    - File : 2D data or 3D data in single file eg: image (2D), video or NIFTI format medical image (3D data in single file)
    - Directory : 3D data in multiple files
  - Slice count : 2d slice number in the task
  - Annotation : a relative path from project data dir. Can be a file or a directory.
    - File: single file annotation
    - Directory : annotation spans multiple files eg: segmentation mask for nifti medical image
  - Date added
  - Last modified
"""


class Task(db.Model):
    __tablename__ = "task"
    __table_args__ = {"comment": "Contains all the tasks"}
    task_id = nncol(db.Integer(), primary_key=True)
    project_id = nncol(db.Integer(), db.ForeignKey("project.project_id"))
    project = db.relationship("Project", backref=db.backref("books")) # TODO: propogate
    data_paths = nncol(db.String())
    label_paths = nncol(db.String())
    slice_count = nncol(db.Integer())
    created = nncol(db.DateTime, default=datetime.utcnow)
    modified = nncol(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 
