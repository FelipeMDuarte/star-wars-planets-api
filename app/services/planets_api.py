import app
import json
from flask import request
from flask_restful import Resource
from app.common import (
    build_response, check_exceptions, POST_INPUT_EXPECTED,
    check_input_json)
from bson import json_util


class PlanetsApi(Resource):
    def get(self, planet_id=None, planet_name=None):
        if planet_id:
            return get_planet_by_id(planet_id)
        if planet_name:
            return get_planet_by_name(planet_name)
        return get_all_planets()  # data, response.status_code

    @check_exceptions
    def post(self):
        received_json = request.json
        check_input_json(received_json, POST_INPUT_EXPECTED)
        return save_new_planet(received_json)

    def put(self):
        return ""  # {}, response.status_code

    def delete(self):
        return ""  # {}, response.status_code


def get_all_planets():
    try:
        results = []
        star_wars_db = app.mongodb.db['star_wars_db']
        for item in star_wars_db.find({}):
            results.append(json.loads(json.dumps(item, default=json_util.default)))
        return results
    except Exception as ex:
        app.app.logger.info("Exception: " + str(ex))
        raise ex

#
# def get_planet_by_id():
#     try:
#         results = []
#         star_wars_db = app.mongodb.db['star_wars_db']
#         for item in star_wars_db.find({}):
#             results.append(dumps(item))
#         return results
#     except Exception as ex:
#         app.app.logger.info("Exception: " + str(ex))
#         raise ex


def save_new_planet(received_json):
    try:
        app.app.logger.info("Json received: " + json.dumps(received_json))
        star_wars_db = app.mongodb.db['star_wars_db']
        star_wars_db.insert_one(received_json)
        app.app.logger.info("Json saved in the database with id: " + str(received_json['_id']))
    except Exception as ex:
        app.app.logger.info("Exception: " + str(ex))
        raise ex
    return build_response(200, "Cadastro realizado com sucesso", str(received_json))
