from flask import Flask, make_response
from flask.ext.sqlalchemy import SQLAlchemy

from workarounds import jsonify


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


@app.route("/")
def hello():
    return "Hello World!"


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    app.run()
