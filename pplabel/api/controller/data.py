import json
import os
import os.path as osp
import base64

import cv2

from pplabel.config import db
from .base import crud
from ..model import Data
from ..schema import DataSchema


get_all, get, post, put, delete = crud(Data, DataSchema)


def get_image(data_id):
    data = Data._get(data_id=data_id)
    path = data.path
    data_dir = data.task.project.data_dir
    data_path = osp.join(data_dir, path)
    image = cv2.imread(data_path)
    image_png = cv2.imencode(".png", image)
    b64_string = base64.b64encode(image_png[1]).decode("utf-8")
    return json.dumps({"image": b64_string}), 200
