from marshmallow import fields


from paddlelabel.api.model import Tag
from .base import BaseSchema


class TagSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Tag
