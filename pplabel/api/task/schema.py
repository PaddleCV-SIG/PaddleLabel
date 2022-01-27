from pplabel.config import ma
from marshmallow import post_load,pre_load , pre_dump, fields
from .model import Task


class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_fk = True
        load_instance = True
    data_paths=fields.List(fields.String())


    @post_load
    def list2str(self, data, **kwargs):
        print("----------", data)
        data_paths_string = ""
        for data_path in data["data_paths"]:
            data_paths_string += data_path + ","
        data["data_paths"] = data_paths_string

        # label_paths_string=""
        # for label_path in data["label_paths"]:
        #     label_paths_string+=(label_path + ",")
        # data["label_paths"]=label_paths_string
        print("data", data)

TaskSchema().load('''{
  "project_id": 1,
  "data_paths": ["data1", "data2"],
  "slice_count": 1
}''')
    # @pre_dump
    # def str2list(self, data, **kwargs):
    #     data['data_paths'] = data['data_paths'].strip(",").split(',')
    #     data['label_paths'] = data['label_paths'].strip(",").split(',')
    #     print("data", data)
