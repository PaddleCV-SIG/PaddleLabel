# -*- coding: utf-8 -*-
from marshmallow import fields, post_dump

from paddlelabel.api.model import Data
from .base import BaseSchema
from paddlelabel.api.schema.util import str2sault


class DataSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Data

    @post_dump
    def post_dump_action(self, data, **kwargs):
        data["sault"] = str2sault(data["path"] + data["created"])
        return data

    # task = fields.Nested("TaskSchema", exclude=("datas", "annotations"))
