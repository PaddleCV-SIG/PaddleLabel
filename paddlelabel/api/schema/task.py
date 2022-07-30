import json
import time

from marshmallow import post_load, pre_load, pre_dump, post_dump, fields
from marshmallow.fields import Nested

from paddlelabel.api.model import Task
from paddlelabel.api.schema.util import path2sault
from .base import BaseSchema


class TaskSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Task

    # project = Nested("ProjectSchema")
    annotations = fields.List(Nested("AnnotationSchema"), exclude=("task",))
    data_paths = fields.List(fields.String())
    # datas = fields.List(Nested("DataSchema"), exclude=("task",))

    # # TODO: confirm data['result'] dont cause trouble
    @pre_dump
    def output(self, task, **kwargs):
        paths = []
        for data in task.datas:
            paths.append(f"/datas/{data.data_id}/image?sault={path2sault(data.path)}")
        task.data_paths = paths
        return task

    # @post_dump
    # def post(self, task, **kwargs):
    #     print("post dump", task)
