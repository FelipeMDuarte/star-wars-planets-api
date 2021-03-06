import app
from flask_restful import Resource
from app.common import check_exceptions, last_tag, last_commit, last_commit_datetime, log_request
from datetime import datetime


class InfoApi(Resource):

    @log_request
    @check_exceptions
    def get(self):
        version = last_commit() if app.config_name != 'production' else last_tag()

        return {
                   "version": version,
                   "commit_datetime": last_commit_datetime(),
                   "server_datetime": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
               }, 200
