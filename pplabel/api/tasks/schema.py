from pplabel.config import ma
from marshmallow import post_load,pre_load , pre_dump, fields
from .model import Task


class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_fk = True
        load_instance = True
    data_paths=fields.List(fields.String())
    label_paths=fields.List(fields.String())
    # @pre_load
    # def check_comma(self,data,**kwargs):
    #     pass

    @post_load
    def list2str(self, data, **kwargs):
        data_paths_string = ""
        for data_path in data["data_paths"]:
            data_paths_string += data_path + ","
        data["data_paths"]=data_paths_string

        label_paths_string=""
        for label_path in data["label_paths"]:
            label_paths_string+=(label_path + ",")
        data["label_paths"]=label_paths_string
        print("data", data)
    
    # @pre_dump
    # def str2list(self, data, **kwargs):
    #     data['data_paths'] = data['data_paths'].strip(",").split(',')
    #     data['label_paths'] = data['label_paths'].strip(",").split(',')
    #     print("data", data)
