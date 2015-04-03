import os
import tempfile

from flask import json

import tsserver


def before_scenario(context, scenario):
    context.db_fd, tsserver.app.config['DATABASE'] = tempfile.mkstemp()
    tsserver.app.config['TESTING'] = True
    context.app = tsserver.app.test_client()

    def request(url, method='GET'):
        """
        Wrapper over Flask.open function that parses returned data as JSON

        :param method: HTTP method to be used. GET is used by default
        :param url: URL to retrieve
        :return: Response object
        """
        rv = context.app.open(url, method=method)
        rv.json_data = json.loads(rv.data)
        return rv

    context.request = request
    tsserver.init_db()


def after_scenario(context, scenario):
    os.close(context.db_fd)
    os.unlink(tsserver.app.config['DATABASE'])
