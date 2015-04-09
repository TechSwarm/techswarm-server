from flask.ext.restful import Resource
from flask.ext.restful import reqparse

from tsserver import models, db, api


class Telemetry(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('temperature', type=float, required=True)
    parser.add_argument('pressure', type=float, required=True)

    def get(self):
        return [x.as_dict() for x in models.Telemetry.query.all()]

    def post(self):
        args = self.parser.parse_args()
        x = models.Telemetry(**args)
        db.session.add(x)
        db.session.commit()
        return x.as_dict(), 201


api.add_resource(Telemetry, '/telemetry')
