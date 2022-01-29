from marshmallow import fields

from pplabel.config import ma, db


class BaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        load_instance = True
        sqla_session = db.session

    immutables = fields.Raw()
