from flask import Flask, jsonify, make_response

import database


app = Flask(__name__)
app.config.from_object('config')


@app.before_request
def init():
    database.connect_db()
    database.init_db()


@app.route("/")
def hello():
    return "Hello World!"


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    app.run()
