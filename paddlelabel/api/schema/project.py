# -*- coding: utf-8 -*-
import json

from marshmallow import pre_load, post_dump, fields

from paddlelabel.api.model import Project
from paddlelabel.api.schema.util import str2sault
from paddlelabel.api.schema.base import BaseSchema


class ProjectSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Project
        # include_relationships = True

    task_category = fields.Nested("TaskCategorySchema")
    labels = fields.List(fields.Nested("LabelSchema"))
    all_options = fields.Dict()

    # TODO: fix these, shouldn't need a _get_other_settings
    # to object
    @pre_load
    def pre_load_action(self, data, **kwargs):
        if "other_settings" in data.keys():
            data["other_settings"] = json.dumps(data["other_settings"])
        return data

    # to string
    @post_dump
    def pre_dump_action(self, project, **kwargs):
        if "other_settings" in project.keys() and project["other_settings"] is not None:
            project["other_settings"] = json.loads(project["other_settings"])
        project["upid"] = str2sault(project["data_dir"] + project["created"])
        return project
