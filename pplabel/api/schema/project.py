from marshmallow import pre_load, fields

# from . import TaskCategorySchema

from pplabel.api.model import Project
from .base import BaseSchema


class ProjectSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Project
        # include_relationships = True

    label_dir = fields.String(allow_none=True)
    task_category = fields.Nested("TaskCategorySchema")
    labels = fields.List(fields.Nested("LabelSchema"))

    # TODO: decorator
    get_task_category = fields.Raw()

    @pre_load
    def pre_load_action(self, data, **kwargs):
        if "label_dir" in data.keys() and data["label_dir"] == "":
            data["label_dir"] = None
        return data
