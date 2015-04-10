from flask.ext.restful import Resource, reqparse

from tsserver import models, db, api
from tsserver.dtutils import timestamp


class Telemetry(Resource):
    getparser = reqparse.RequestParser()
    getparser.add_argument('since', type=timestamp)

    postparser = reqparse.RequestParser()
    postparser.add_argument('timestamp', type=timestamp, required=True)
    postparser.add_argument('temperature', type=float, required=True)
    postparser.add_argument('pressure', type=float, required=True)

    def get(self):
        args = self.getparser.parse_args()
        filter_args = []
        if args['since'] is not None:
            filter_args += [models.Telemetry.timestamp > args['since']]
        return [x.as_dict() for x in
                models.Telemetry.query.filter(*filter_args).all()]

    def post(self):
        args = self.postparser.parse_args()
        x = models.Telemetry(**args)
        db.session.add(x)
        db.session.commit()
        return x.as_dict(), 201


api.add_resource(Telemetry, '/telemetry')
