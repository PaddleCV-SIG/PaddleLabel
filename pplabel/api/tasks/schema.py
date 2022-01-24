from pplabel.config import ma
from .model import Project


class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        include_fk = True
        load_instance = True
