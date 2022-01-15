from flask import Blueprint
from flask_restful import Api

from .routes import init_routes


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

init_routes(api)
