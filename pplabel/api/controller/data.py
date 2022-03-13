import json
import os
import os.path as osp
import base64

import cv2
import flask

from pplabel.config import db
from .base import crud
from ..model import Data
from ..schema import DataSchema


get_all, get, post, put, delete = crud(Data, DataSchema)

# TODO: directly return binary stream, use mime as type. dont base64
def get_image(data_id):
    data = Data._get(data_id=data_id)
    path = data.path
    data_dir = data.task.project.data_dir
    return flask.send_from_directory(data_dir, path)

    data_path = osp.join(data_dir, path)

    # print("data_pathdata_pathdata_pathdata_path", data_path)
    # image = cv2.imread(data_path)
    # image_png = cv2.imencode(".png", image)
    # b64_string = base64.b64encode(image_png[1]).decode("utf-8")
    # return json.dumps({"image": b64_string}), 200
