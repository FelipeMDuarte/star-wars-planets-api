from flask_restful import Resource
import app


class HealthApi(Resource):

    def get(self):
        app.logger.info(status=200, message="/healthcheck esta ok.")
        return "", 200
