import app
import json
import requests
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
        return get_all_planets()

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
        json_to_save = dict()
        json_to_save = received_json
        json_to_save['films'] = get_films(json_to_save['name'])
        star_wars_db.insert_one(received_json)
        app.app.logger.info("Json saved in the database with id: " + str(received_json['_id']))
    except Exception as ex:
        app.app.logger.info("Exception: " + str(ex))
        raise ex
    return build_response(200, "Cadastro realizado com sucesso", str(received_json))


def update_planet(received_json, planet_name_id):
    try:
        app.app.logger.info("Json received: " + json.dumps(received_json))
        star_wars_db = app.mongodb.db['star_wars_db']
        json_to_save = dict()
        json_to_save = received_json
        json_to_save['films'] = get_films(json_to_save['name'])

        if hasNumbers(planet_name_id):
            updated = star_wars_db.find_one_and_update({"_id":ObjectId(planet_name_id)},{"$set":received_json})
        else:
            updated = star_wars_db.find_one_and_update({"name":planet_name_id},{"$set":received_json})
        if not updated:
            app.app.logger.info("Planet not found: " + str(planet_name_id))
            return build_response(404, "O planeta enviado nao foi encontrado: " + str(planet_name_id), "")
        app.app.logger.info("Updated planet in the database: " + str(planet_name_id))
        return build_response(200, "Update realizado com sucesso", "")

    except Exception as ex:
        app.app.logger.info("Exception: " + str(ex))
        raise ex


def delete_planet(planet_name_id):
    try:
        app.app.logger.info("Dado recebido para deletar: " + str(planet_name_id))
        star_wars_db = app.mongodb.db['star_wars_db']
        if hasNumbers(planet_name_id):
            deleted = star_wars_db.remove({"_id": ObjectId(planet_name_id)})
        else:
            deleted = star_wars_db.remove({"name": planet_name_id})
        print("@@@@ - ", deleted)
        if deleted['n'] == 0:
            app.app.logger.info("Planet not found: " + str(planet_name_id))
            return build_response(
                404, "O planeta enviado nao foi encontrado: " + str(planet_name_id), "")
        app.app.logger.info("Deleted planet in the database: " + str(planet_name_id))
        return build_response(200, "Delete realizado com sucesso", "")
    except Exception as ex:
        app.app.logger.info("Exception: " + str(ex))
        raise ex


def serialize_mongo_result(item):
    return json.loads(json.dumps(item, default=json_util.default))


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def get_films(planet_name):
    response = requests.get("https://swapi.co/api/planets/?search="+planet_name)
    response = response.json()
    if response["count"] > 1:
        raise Exception("Foram achados mais de um planeta com o nome enviado")
    if response["count"] == 0:
        raise Exception("Nao foi achado nenhum planeta com o nome enviado")
    films = len(response['results'][0]['films'])
    return films or 0
