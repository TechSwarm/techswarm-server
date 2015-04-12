from datetime import datetime
from io import BytesIO
import os
import shutil

from behave import *

from tsserver import db, models, configutils
from tsserver.dtutils import datetime_to_str
from tsserver.features.testutils import (
    open_resource, resource_path, parse_data_table_row
)


@given("test photos in upload directory")
def step_impl(context):
    src = os.path.join(resource_path(), 'deathvalley.jpg')
    uploads = configutils.get_upload_dir()
    for filename in {'test001.jpg', 'test002.jpg'}:
        shutil.copyfile(src, os.path.join(uploads, filename))


@given("following photo data")
def step_impl(context):
    for row in context.table:
        d = parse_data_table_row(row)
        x = models.Photo(**d)
        db.session.add(x)
    db.session.commit()


@then("list of {num:d} object with image details should be sent")
@then("list of {num:d} objects with image details should be sent")
def step_impl(context, num):
    assert len(context.rv.json_data) == num
    assert all({'id', 'filename', 'url', 'timestamp'} == set(x)
               for x in context.rv.json_data)


@when("I upload an image to {url}")
def step_impl(context, url):
    data = {'timestamp': datetime_to_str(datetime.now()),
            'photo': (open_resource('deathvalley.jpg', mode='rb'),
                      'TEST_ONLY_deathvalley.jpg')}
    context.rv = context.request(url, 'POST', data=data)


@then("JSON with image details should be sent")
def step_impl(context):
    assert {'id', 'filename', 'url', 'timestamp'} == set(context.rv.json_data)
    # Save the photo filename so it can be later removed
    context.test_photo_url = context.rv.json_data['filename']


@when('I request file from "{key}" key')
def step_impl(context, key):
    context.rv = context.app.get(context.rv.json_data[key])


@when("I upload a file with '{ext}' extension to {url}")
def step_impl(context, ext, url):
    data = {'timestamp': datetime_to_str(datetime.now()),
            'photo': (BytesIO(b'test'), 'example.' + ext)}
    context.rv = context.request(url, 'POST', data=data)
