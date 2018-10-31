import os
from flask import Flask
from config import config
from flask_restful import Api
from .common import dictConfig
from .dependencies_api import DependencyApi
from .services import ServiceApi, HealthApi, WorkApi, InfoApi, PlanetsApi

config_name = os.environ.get('ENVIRONMENT')

dictConfig = dictConfig

app = Flask(__name__)
app.config.from_object(config[config_name])

api = Api(app, prefix="/api")

dependency_api = DependencyApi(app.config['DEPENDENCY_API_A_URL'])
another_dependency_api = DependencyApi(app.config['DEPENDENCY_API_B_URL'])

api.add_resource(ServiceApi, "/service")
api.add_resource(HealthApi, "/healthcheck")
api.add_resource(WorkApi, "/working")
api.add_resource(InfoApi, "/info")
api.add_resource(PlanetsApi, "/planets")
