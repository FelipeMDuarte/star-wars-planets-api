import app
import json
from flask import request
from flask_restful import Resource


class PlanetsApi(Resource):
    def get(self):
        return ""  # data, response.status_code

    def post(self):
        received_json = request.json
        return save_new_planet(received_json)

    def put(self):
        return ""  # {}, response.status_code

    def delete(self):
        return ""  # {}, response.status_code


def save_new_planet(received_json):
    try:
        app.app.logger.info("Json received: " + json.dumps(received_json))
        star_wars_db = app.mongodb.db['star_wars_db']
        star_wars_db.insert_one(received_json)
        app.app.logger.info("Json saved in the database with id: " + str(received_json['_id']))
    except Exception as ex:
        app.app.logger.info("Exception: " + str(ex))
        raise ex
    return "", 200
