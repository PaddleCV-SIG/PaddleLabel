from paddlelabel.config import ma, db


class BaseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        load_instance = True
        sqla_session = db.session
