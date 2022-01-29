from marshmallow import post_load, pre_load, pre_dump, fields
from marshmallow_sqlalchemy.fields import Nested

from pplabel.config import ma
from .model import Annotation


class AnnotationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Annotation
        include_fk = True
        load_instance = True

    task = Nested("TaskSchema", exclude=("annotations",))
