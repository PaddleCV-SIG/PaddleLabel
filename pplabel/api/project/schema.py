from marshmallow import pre_load

from pplabel.config import ma
from .model import Project


class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        include_relationships = True
        load_instance = True
    label_dir = ma.String(allow_none=True)


    @pre_load
    def empty_label_dir(self, data, **kwargs):
        if 'label_dir' in data.keys() and data['label_dir'] == "":
            data['label_dir'] = None
        return data
