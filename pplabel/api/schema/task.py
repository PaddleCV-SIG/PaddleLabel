import json

from marshmallow import post_load, pre_load, pre_dump, fields
from marshmallow.fields import Nested

from pplabel.api.model import Task
from .base import BaseSchema


class TaskSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Task

    project = Nested("ProjectSchema")
    annotations = fields.List(Nested("AnnotationSchema"), exclude=("task",))

    # TODO: check invalid chars in path
    @pre_load
    def list2str(self, data, **kwargs):
        datas = []
        for path in data["datas"]:
            datas.append({"path": path})
        data["datas"] = datas
        return data

    # TODO: confirm data['result'] dont cause trouble
    @pre_dump
    def output(self, data, **kwargs):
        return data

    # @post_load
    # def list2str(self, data, **kwargs):
    #     data["data_paths"].sort()  # TODO: custom sort for each scene
    #     data_paths_string = ""
    #     for data_path in data["data_paths"]:
    #         data_paths_string += data_path + ","
    #     data["data_paths"] = data_paths_string
    #     return data
    #
    # @pre_dump
    # def str2list(self, data, **kwargs):
    #     data_path_string = data.data_paths
    #     data_path_string = data_path_string.split(",")
    #     data_paths = []
    #     for path in data_path_string:
    #         if len(path) != 0:
    #             data_paths.append(path)
    #     data.data_paths = data_paths
    #     return data


# TaskSchema().load('''{
#   "project_id": 1,
#   "data_paths": ["data1", "data2"],
#   "slice_count": 1
# }''')
# @pre_dump
# def str2list(self, data, **kwargs):
#     data['data_paths'] = data['data_paths'].strip(",").split(',')
#     data['label_paths'] = data['label_paths'].strip(",").split(',')
#     print("data", data)
