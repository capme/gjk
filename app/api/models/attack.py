from app.db import db
from typing import List


class AttackModel(db.Model):
    """
    Attack model
    """
    __tablename__ = "attack"
    __table_args__ = ({'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_0900_ai_ci'}, )

    id = db.Column(db.Integer, primary_key=True)
    attack_name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, attack_name):
        self.attack_name = attack_name

    def __repr__(self):
        return "<AttackModel {}>".format(self.attack_name)

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all(cls) -> List["AttackModel"]:
        return cls.query.all()
