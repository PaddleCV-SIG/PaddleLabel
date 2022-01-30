from pplabel.api.model import Label
from .base import BaseSchema


class LabelSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Label
