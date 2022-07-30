from marshmallow import fields

from paddlelabel.api.model import Label
from .base import BaseSchema


class LabelSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Label

    id = fields.Integer()
