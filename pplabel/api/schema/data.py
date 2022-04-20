from marshmallow import fields, post_dump

from pplabel.api.model import Data
from .base import BaseSchema
from pplabel.api.schema.util import path2sault


class DataSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Data

    @post_dump
    def post_dump_action(self, data, **kwargs):
        data["sault"] = path2sault(data["path"])
        return data

    # task = fields.Nested("TaskSchema", exclude=("datas", "annotations"))
