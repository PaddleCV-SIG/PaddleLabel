from marshmallow import fields


from pplabel.api.model import TagTask
from .base import BaseSchema


class TagTaskSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = TagTask
