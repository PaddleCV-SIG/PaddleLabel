from marshmallow import pre_load, pre_dump, fields

from .model import Project
from ..setting import TaskCategory
import pplabel
from pplabel.config import ma, db
from pplabel.api.setting.schema import TaskCategorySchema


class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        # include_relationships = True
        include_fk = True
        load_instance = True
        sqla_session = db.session

    label_dir = ma.String(allow_none=True)
    task_category = fields.Nested(TaskCategorySchema)
    label_config = fields.Raw()

    @pre_load
    def pre_load_action(self, data, **kwargs):
        if "label_dir" in data.keys() and data["label_dir"] == "":
            data["label_dir"] = None
        label_config = data.get("label_config", None)
        if label_config is not None:
            task_category = TaskCategory.query.filter(
                TaskCategory.task_category_id == data["task_category_id"]
            ).one()
            data["label_config"] = eval(task_category.handler)().load(label_config)
        return data

    # @pre_dump
    # def pre_dump_action(self, data, **kwargs):
    #     # data["label_config"] = ""
    #     # print("aaaaaaaaaaaaaaaaa", data)
    #     return data
