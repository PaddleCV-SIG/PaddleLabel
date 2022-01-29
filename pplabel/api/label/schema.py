from ..base import BaseSchema
from .model import Label


class LabelSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Label
