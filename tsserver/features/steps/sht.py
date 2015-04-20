from datetime import datetime

from behave import *
from decimal import Decimal

from tsserver.dtutils import datetime_to_str
from tsserver.features.testutils import table_to_database
from tsserver.genericapi.models import SHT


example_telemetry_data = {
    'timestamp': datetime(1970, 1, 1),
    'humidity': Decimal('66.6'),
    'temperature': Decimal('23.6')
}


@when("I POST example SHT data")
def step_impl(context):
    data = example_telemetry_data.copy()
    data['timestamp'] = datetime_to_str(data['timestamp'])
    context.rv = context.request('/sht', 'POST', data=data)


@then("example SHT data should be saved to the database")
def step_impl(context):
    assert SHT.query.count() == 1
    assert SHT.query.all()[0].serializable == example_telemetry_data


@when("I POST example SHT data without {parameter}")
def step_impl(context, parameter):
    data = example_telemetry_data.copy()
    data.pop(parameter)
    context.rv = context.request('/sht', 'POST', data=data)


@given("following SHT data")
def step_impl(context):
    table_to_database(context.table, SHT)
