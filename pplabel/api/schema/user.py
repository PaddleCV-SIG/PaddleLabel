from marshmallow import pre_load, fields

from pplabel.api.model import User
from .base import BaseSchema


class UserSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = User
