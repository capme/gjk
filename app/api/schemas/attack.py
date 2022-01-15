from app.api.models.attack import AttackModel
from app.ma import ma


class AttackSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AttackModel
        load_instance = True
        dump_only = ("id",)
        ordered = True
        include_fk = True
