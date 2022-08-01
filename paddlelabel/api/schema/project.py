import json

from marshmallow import pre_load, post_dump, fields

from paddlelabel.api.model import Project
from .base import BaseSchema


class ProjectSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Project
        # include_relationships = True

    label_dir = fields.String(allow_none=True)
    task_category = fields.Nested("TaskCategorySchema")
    labels = fields.List(fields.Nested("LabelSchema"))

    @pre_load
    def pre_load_action(self, data, **kwargs):
        if "label_dir" in data.keys() and data["label_dir"] == "":
            data["label_dir"] = None

        if "other_settings" in data.keys():
            data["other_settings"] = json.dumps(data["other_settings"])
        return data

    @post_dump
    def pre_dump_action(self, project, **kwargs):
        if "other_settings" in project.keys() and project["other_settings"] is not None:
            project["other_settings"] = json.loads(project["other_settings"])
        # print(project["other_settings"])
        return project
