from datetime import datetime

from behave import *

from tsserver.dtutils import datetime_to_str
from tsserver.features.testutils import table_to_database
from tsserver.genericapi.models import Status


@given("following status data")
def step_impl(context):
    table_to_database(context.table, Status)


@given("no status data in database")
def step_impl(context):
    Status.query.delete()
    assert Status.query.count() == 0


@when("I {method} mission phase {phase} in '{parameter}' parameter to {url}")
def step_impl(context, method, phase, parameter, url):
    context.rv = context.request(url, method, data={
        'timestamp': datetime_to_str(datetime(2000, 1, 1)),
        'connected': True,
        parameter: phase
    })
