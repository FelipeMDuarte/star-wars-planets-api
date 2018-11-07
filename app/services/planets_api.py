import app
import json
from flask import request
from flask_restful import Resource
from app.common import (
    build_response, check_exceptions, POST_INPUT_EXPECTED,
    check_input_json, PUT_INPUT_EXPECTED)
from bson import json_util
from bson.objectid import ObjectId


class PlanetsApi(Resource):

    def get(self, planet_name_id=None):
        if planet_name_id:
            return get_planet_by_name_id(planet_name_id)
        return get_all_planets()  # data, response.status_code

    @check_exceptions
    def post(self):
        received_json = request.json
        check_input_json(received_json, POST_INPUT_EXPECTED)
        return save_new_planet(received_json)

    def put(self, planet_name_id):
        received_json = request.json
        check_input_json(received_json, PUT_INPUT_EXPECTED)
        return update_planet(received_json, planet_name_id)

    def delete(self, planet_name_id):
        return delete_planet(planet_name_id)


def get_all_planets():
    try:
        results = []
        star_wars_db = app.mongodb.db['star_wars_db']
        for item in star_wars_db.find({}):
            results.append(serialize_mongo_result(item))
        return results
    except Exception as ex:
        app.app.logger.info("Exception: " + str(ex))
        raise ex


def serialize_mongo_result(item):
    return json.loads(json.dumps(item, default=json_util.default))


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def get_planet_by_name_id(planet_name_id):
    try:
        star_wars_db = app.mongodb.db['star_wars_db']
        if hasNumbers(planet_name_id):
            for item in star_wars_db.find({"_id": ObjectId(planet_name_id)}):
                return serialize_mongo_result(item)
        for item in star_wars_db.find({"name": planet_name_id}):
            return serialize_mongo_result(item)
    except Exception as ex:
        app.app.logger.info("Exception: " + str(ex))
        raise ex


def save_new_planet(received_json):
    try:
        app.app.logger.info("Json received: " + json.dumps(received_json))
        star_wars_db = app.mongodb.db['star_wars_db']
        # TODO Fazer request na starwars api pela quantidade de apariçoes nos filmes
        star_wars_db.insert_one(received_json)
        app.app.logger.info("Json saved in the database with id: " + str(received_json['_id']))
    except Exception as ex:
        app.app.logger.info("Exception: " + str(ex))
        raise ex
    return build_response(200, "Cadastro realizado com sucesso", str(received_json))

def update_planet(received_json, planet_id):
    try:
        app.app.logger.info("Json received: " + json.dumps(received_json))
        star_wars_db = app.mongodb.db['star_wars_db']
        # TODO Fazer request na starwars api pela quantidade de apariçoes nos filmes
        star_wars_db.find_one_and_update({"_id":ObjectId(planet_id)},{"$set":received_json})
        app.app.logger.info("Updated planet in the database with id: " + str(planet_id))
    except Exception as ex:
        app.app.logger.info("Exception: " + str(ex))
        raise ex
    return build_response(200, "Update realizado com sucesso", "")

def delete_planet(planet_id):
    try:
        app.app.logger.info("Id recebido para deletar: "+ str(planet_id))
        star_wars_db = app.mongodb.db['star_wars_db']
        star_wars_db.remove({"_id":ObjectId(planet_id)})
        app.app.logger.info("Deleted planet in the database with id: " + str(planet_id))
    except Exception as ex:
        app.app.logger.info("Exception: " + str(ex))
        raise ex
    return build_response(200, "Delete realizado com sucesso", "")
