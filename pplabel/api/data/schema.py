from marshmallow import post_load, pre_load, pre_dump, fields
from marshmallow_sqlalchemy.fields import Nested

from pplabel.serve import ma

# from .model import Task
from .model import Data


class DataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Data
        include_fk = True
        load_instance = True

    # task = fields.Nested("TaskSchema", exclude=("datas",))
