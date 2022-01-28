from marshmallow import post_load, pre_load, pre_dump, fields
from marshmallow_sqlalchemy.fields import Nested


from pplabel.config import ma

# from .model import Task
from pplabel.api.model import Task
from pplabel.api.project.schema import ProjectSchema


class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_fk = True
        load_instance = True

    data_paths = fields.List(fields.String())
    project = Nested(ProjectSchema)

    # TODO: invalid chars
    @post_load
    def list2str(self, data, **kwargs):
        data["data_paths"].sort()  # TODO: custom sort for each scene
        data_paths_string = ""
        for data_path in data["data_paths"]:
            data_paths_string += data_path + ","
        data["data_paths"] = data_paths_string
        return data

    @pre_dump
    def str2list(self, data, **kwargs):
        data_path_string = data.data_paths
        data_path_string = data_path_string.split(",")
        data_paths = []
        for path in data_path_string:
            if len(path) != 0:
                data_paths.append(path)
        data.data_paths = data_paths
        return data


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
