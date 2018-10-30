from flask_restful import Resource
import app


class HealthApi(Resource):

    def get(self):
        app.log.info(status=200, message="/healthcheck esta ok.")
        return "", 200
