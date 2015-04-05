from flask import Flask, jsonify, make_response
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy()


@app.before_request
def init():
    # Database is initialized here, since database config can be changed
    # after importing this file (such as in testing), but before actually doing
    # anything with the database
    db.init_app(app)


@app.route("/")
def hello():
    return "Hello World!"


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    app.run()
