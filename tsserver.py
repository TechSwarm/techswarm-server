from flask import Flask, jsonify, make_response

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': "Not found"}), 404)


def init_db():
    pass


if __name__ == "__main__":
    app.run()
