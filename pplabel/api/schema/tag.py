from marshmallow import fields


from pplabel.api.model import Tag
from .base import BaseSchema


class TagSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Tag
