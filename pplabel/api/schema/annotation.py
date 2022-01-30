from marshmallow import fields


from pplabel.api.model import Annotation
from .base import BaseSchema


class AnnotationSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Annotation

    project_id = fields.Integer()
    # task = Nested("TaskSchema", exclude=("annotations",))
    label = fields.Nested("LabelSchema")
