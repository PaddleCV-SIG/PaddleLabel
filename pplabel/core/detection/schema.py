from marshmallow import Schema, fields

from pplabel.config import ma, db


class LabelConfig(Schema):
    classes = fields.List(fields.String(), allow_none=True)
    multi_class = fields.Bool()
