from flask import request
from flask_restful import Resource
from app.api.models.attack import AttackModel
from app.api.schemas.attack import AttackSchema


attacks_schema = AttackSchema(many=True)
attack_schema = AttackSchema()


class Attacks(Resource):
    def get(self):
        return attacks_schema.dump(AttackModel.find_all()), 200


class Attack(Resource):
    @classmethod
    def post(cls):
        attack = attack_schema.load(request.get_json())
        attack.add_to_db()
        return {'msg': 'The attack activity has been created', 'attack_id': attack.id}, 201
