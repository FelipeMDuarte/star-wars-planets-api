from behave import Given, then, given
import json
import mongomock
import app
from unittest.mock import MagicMock
from pymongo import MongoClient


@Given('I create a mongodb mock object')
def json_mock(context):
    context.app_mongodb = app.mongodb
    app.mongodb = mongomock.MongoClient(port=27019)


@then('I reset the mongodb mock object')
def reset_json_mock(context):
    app.mongodb = context.app_mongodb


@Given('I save a job json in the mongodb')
def json_save_mock(context):
    json_planet = json.loads(context.text)
    planet = app.mongodb.db.star_wars_db.insert(json_planet)
    context.planet_id = str(planet)


@given('I mock pymongo healthcheck')
def mock_pymongo(context):
    context.pymongo_serverinfo = MongoClient.server_info
    MongoClient.server_info = MagicMock(return_value=True)


@then('I reset pymongo mock')
def reset_mock_pymongo(context):
    MongoClient.server_info = context.pymongo_serverinfo
