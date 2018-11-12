from flask_restful import Resource
import app


class HealthApi(Resource):

    def get(self):
        app.app.logger.info("/healthcheck esta ok.")
        return "", 200
