import hashlib


from marshmallow import fields, post_dump

from pplabel.api.model import Data
from .base import BaseSchema


class DataSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Data

    @post_dump
    def post_dump_action(self, data, **kwargs):
        data["sault"] = hashlib.md5(data["path"].encode("utf-8")).hexdigest()[:10]
        return data

    # task = fields.Nested("TaskSchema", exclude=("datas", "annotations"))
