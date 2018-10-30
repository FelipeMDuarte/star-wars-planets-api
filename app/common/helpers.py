import json
from flask import request
from jsonschema import validate, ValidationError
import subprocess
import app
from threading import Thread


class ValidateInput(object):
    def __init__(self, json_schema):
        self.json_schema = json_schema

    def __call__(self, original_func):
        def wrappee(*args, **kwargs):
            try:
                if not hasattr(request, 'json'):
                    raise ValidationError('No json provided.')
                validate(request.json, json.loads(self.json_schema))
            except ValidationError as ex:
                raise InvalidInputError('URL: ' + request.full_path
                                        + ' - BODY: ' + request.data.decode("utf-8") + ''
                                        + ' - ERROR: ' + str(ex))
            return original_func(*args, **kwargs)

        return wrappee


def check_json(json_expected, json_response):
    if type(json_expected) is list:
        for i in range(0, len(json_expected)):
            check_json(json_expected[i], json_response[i])
            check_json(json_response[i], json_expected[i])
    elif type(json_expected) is dict:
        for key, value in json_expected.items():
            if type(value) is dict:
                assert_that(json_response, has_key(key))
                check_json(value, json_response[key])
                check_json(json_response[key], value)
            elif type(value) is list:
                for i in range(0, len(value)):
                    check_json(json_expected[key][i], json_response[key][i])
                    check_json(json_response[key][i], json_expected[key][i])
            else:
                assert_that(json_response, has_entry(key, value))
    else:
        assert_that(json_response, equal_to(json_expected))


def check_exceptions(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except BaseCipError as ex:
            app.log.error(ex.code, ex.http_status, message=ex.message)
            return ex.get_friendly_message_json(), ex.http_status
        except Exception as ex:
            ex = GeneralUnexpectedError(app.app.config['SERVICE_NAME'], str(ex))
            app.log.error(ex.code, ex.http_status, message=ex.message)
            return ex.get_friendly_message_json(), ex.http_status

    return wrapper


def build_response(error_code, message, response, status_code):
    return {
        "error_code": error_code,
        "message": message,
        "response": response
    }, status_code


def build_working_response(service, status, error_description='', error_code=''):
    return {
        "service": service,
        "status": status,
        "error_description": error_description,
        "error_code": error_code
    }


def log_request(f):
    def wrapper(*args, **kwargs):
        message = "Method: " + str(request.method) + " endpoint: " + request.full_path + " body: "
        if request.data:
            message += str(request.data)

        app.log.info(200, message='Request recebido: ' + message)
        response = f(*args, **kwargs)
        return response
    return wrapper


def process_async(async_function):
    def decorator(f):
        def wrapper(*args, **kwargs):
            thread = Thread(target=async_function, args=args, kwargs=kwargs)
            thread.start()
            return f(*args, **kwargs)
        return wrapper
    return decorator


def last_commit():
    """Return last commit and your date"""
    return subprocess.check_output(['git', 'log', '-1', '--pretty=format:"%h"'],
                                   universal_newlines=False).decode("utf-8").replace('\"', '')


def last_commit_datetime():
    """Return last commit and your date"""
    return subprocess.check_output(['git', 'log', '-1', '--pretty=format:"%cd"'],
                                   universal_newlines=False).decode("utf-8").replace('\"', '')


def last_tag():
    """Return last tag"""
    return app.app.config['GIT_TAG']
