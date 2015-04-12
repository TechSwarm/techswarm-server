import os
import tempfile

from flask import json

import tsserver
from tsserver import configutils



# If set to True, each time the test is run, new database is created as a
# temporary file. If the value is equal to False, tests will be using SQLite
# in-memory database.
USE_DB_TEMP_FILE = False


def before_scenario(context, scenario):
    if USE_DB_TEMP_FILE:
        context.db_fd, context.db_url = tempfile.mkstemp()
        db_url = 'sqlite:///' + context.db_url
    else:
        db_url = 'sqlite://'
    tsserver.app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    # Ensure the tests are actually run in temporary database
    assert str(tsserver.db.engine.url) == db_url

    tsserver.app.config['TESTING'] = True
    tsserver.db.create_all()
    context.app = tsserver.app.test_client()

    def request(url, method='GET', *args, **kwargs):
        """
        Wrapper over Flask.open function that parses returned data as JSON

        :param method: HTTP method to be used. GET is used by default
        :param url: URL to retrieve
        :return: Response object
        """
        rv = context.app.open(url, method=method, *args, **kwargs)
        rv.json_data = json.loads(rv.data)
        return rv

    context.request = request


def remove_uploaded(filename):
    path = os.path.join(configutils.get_upload_dir(), filename)
    if os.path.isfile(path):
        os.remove(path)


def after_scenario(context, scenario):
    tsserver.db.session.remove()
    tsserver.db.drop_all()
    if USE_DB_TEMP_FILE:
        os.close(context.db_fd)
        os.unlink(context.db_url)

    # If test photo was uploaded, remove it
    if 'test_photo_url' in context:
        remove_uploaded(context.test_photo_url)


def after_all(context):
    # Remove uploaded images
    remove_uploaded('test001.jpg')
    remove_uploaded('test002.jpg')
