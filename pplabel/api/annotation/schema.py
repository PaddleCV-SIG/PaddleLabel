from marshmallow.fields import Nested

from ..base import BaseSchema
from .model import Annotation


class AnnotationSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Annotation

    # task = Nested("TaskSchema", exclude=("annotations",))
    label = Nested("LabelSchema")
