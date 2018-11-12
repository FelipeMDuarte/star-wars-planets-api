import app
from flask_restful import Resource
from app.common import check_exceptions, build_working_response
import pymongo


class WorkApi(Resource):

    @check_exceptions
    def get(self):

        app.app.logger.info('/working esta ok.')
        work_list = []
        try:
            maxSevSelDelay = 1000
            client = pymongo.MongoClient(app.app.config['MONGO_URI'],
                                         serverSelectionTimeoutMS=maxSevSelDelay)
            client.server_info()
            work_list.append(build_working_response('mongo-db', 'working'))
        except Exception as ex:
            work_list.append(build_working_response(
                'mongo-db', 'error', "Database timeout.", "DBE001"))

        return work_list, 200
