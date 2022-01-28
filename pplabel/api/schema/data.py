from marshmallow import post_load, pre_load, pre_dump, fields
from marshmallow_sqlalchemy.fields import Nested

from pplabel.config import ma

# from .model import Task
from ..model import Data


class DataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Data
        include_fk = True
        load_instance = True

    # @pre_load(pass_many=True)
    # def list2json(self, data, many, **kwargs):
    #     print("9999999999999", data)
    #     print("1111111111111", many)
    #     datas = []
    #     for path in data:
    #         datas.append({"path": path})
    #     print("000000000", datas)
    #     return datas
