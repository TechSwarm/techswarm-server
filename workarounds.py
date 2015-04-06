from flask.globals import current_app, request
from flask.json import dumps


def jsonify(*args, **kwargs):
    """
    Implementation of :method:`flask.json.jsonify` that allows to jsonify
    arrays, and not only dictionaries.

    Proper support for this is going to be added in Flask at some point in
    the future (1.0, probably). As soon as it works properly there, this
    workaround function should be removed. For more informations about why
    there is such limitation in Flask, as well as why and when it will be
    removed, see:

    * https://github.com/mitsuhiko/flask/issues/248
    * https://github.com/mitsuhiko/flask/pull/1402
    """
    indent = None
    if (current_app.config['JSONIFY_PRETTYPRINT_REGULAR']
            and not request.is_xhr):
        indent = 2
    data = list(*args)
    if not data:
        data = kwargs
    json = dumps(data, indent=indent)
    return current_app.response_class(json, mimetype='application/json')
