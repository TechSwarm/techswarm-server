from flask import Flask, make_response, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import Api, Resource, reqparse


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
api = Api(app)

import models


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


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    app.run(debug=True)
