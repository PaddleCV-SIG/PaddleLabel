from marshmallow.fields import Nested


from pplabel.api.model import Annotation
from .base import BaseSchema


class AnnotationSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Annotation

    # task = Nested("TaskSchema", exclude=("annotations",))
    label = Nested("LabelSchema")
