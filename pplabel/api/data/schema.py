from .model import Data
from ..base import BaseSchema


class DataSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Data

    # task = fields.Nested("TaskSchema", exclude=("datas",))
