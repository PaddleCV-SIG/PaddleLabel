from marshmallow import Schema, fields

from pplabel.serve import ma, db


class LabelConfig(Schema):
    classes = fields.List(fields.String(), allow_none=True)
    multi_class = fields.Bool()
