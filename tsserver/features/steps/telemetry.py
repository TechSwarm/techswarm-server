from datetime import datetime

from behave import *

from tsserver.dtutils import datetime_to_str
from tsserver.features.testutils import table_to_database
from tsserver.genericapi.models import Telemetry


example_telemetry_data = {
    'timestamp': datetime_to_str(datetime(1970, 1, 1)),
    'temperature': 23.6,
    'pressure': 1000
}


@when("I POST example telemetry data")
def step_impl(context):
    context.rv = context.request('/telemetry', 'POST',
                                 data=example_telemetry_data)


@then("example telemetry data should be saved to the database")
def step_impl(context):
    assert Telemetry.query.count() == 1
    assert Telemetry.query.all()[0].serializable == example_telemetry_data


@when("I POST example telemetry data without {parameter}")
def step_impl(context, parameter):
    data = example_telemetry_data.copy()
    data.pop(parameter)
    context.rv = context.request('/telemetry', 'POST', data=data)


@given("following telemetry data")
def step_impl(context):
    table_to_database(context.table, Telemetry)
