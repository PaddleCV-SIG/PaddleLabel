from marshmallow_sqlalchemy import SQLAlchemySchema, SQLAlchemySchemaOpts

from pplabel.config import session


class BaseOpts(SQLAlchemySchemaOpts):
    def __init__(self, meta, ordered=False):
        if not hasattr(meta, "sqla_session"):
            meta.sqla_session = session
            # deserialize to class instance, False would be to dictionary
            meta.load_instance = True
        super(BaseOpts, self).__init__(meta, ordered=ordered)


class BaseSchema(SQLAlchemySchema):
    OPTIONS_CLASS = BaseOpts
