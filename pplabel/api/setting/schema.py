from marshmallow import pre_load, fields

from pplabel.config import ma, db
from pplabel.core.classification import LabelConfig
from . import TaskCategory


class TaskCategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TaskCategory
        include_relationships = True
        load_instance = True
        sqla_session = db.session
