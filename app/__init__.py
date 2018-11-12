import os
from flask import Flask
from config import config
from flask_restful import Api
from .common import dictConfig
from flask_pymongo import PyMongo
from .services import HealthApi, WorkApi, InfoApi, PlanetsApi

config_name = os.environ.get('ENVIRONMENT')

dictConfig = dictConfig

app = Flask(__name__)
app.config.from_object(config[config_name])

api = Api(app, prefix="/api")

mongodb = PyMongo(app)

api.add_resource(HealthApi, "/healthcheck")
api.add_resource(WorkApi, "/working")
api.add_resource(InfoApi, "/info")
api.add_resource(PlanetsApi, "/planets",
                             "/planets/<string:planet_name_id>")


@app.route("/")
def get():
    return "Welcome to the dark side. \nThe api links are: \n/api/planets to list all or add one\n/api/planets/name-or-id to get one, update one or delete."
