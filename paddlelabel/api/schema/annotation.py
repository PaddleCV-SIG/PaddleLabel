from marshmallow import fields


from paddlelabel.api.model import Annotation
from .base import BaseSchema


class AnnotationSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Annotation

    # not required when calling api
    project_id = fields.Integer()
    task_id = fields.Integer()
    # task = fields.Nested("TaskSchema", exclude=("annotations", "datas"))
    label = fields.Nested("LabelSchema")
