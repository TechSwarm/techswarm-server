from flask import make_response, jsonify

from tsserver import app


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': "Not found"}), 404)
