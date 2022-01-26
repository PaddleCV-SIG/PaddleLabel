from marshmallow import pre_load

from pplabel.config import ma
from .model import Project


# class BaseSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         include_relationships = True
#         load_instance = True
#     to_none =
#
#     @pre_load
#     def empty2none(self, data, **kwargs):
#         if 'label_dir' in data.keys() and data['label_dir'] == "":
#             data['label_dir'] = None
#         return data
