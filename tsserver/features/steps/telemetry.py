from datetime import datetime

from behave import *

from tsserver import db
from tsserver.dtutils import datetime_from_str, datetime_to_str
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
    assert Telemetry.query.all()[0].as_dict() == example_telemetry_data


@when("I POST example telemetry data without {parameter}")
def step_impl(context, parameter):
    data = example_telemetry_data.copy()
    data.pop(parameter)
    context.rv = context.request('/telemetry', 'POST', data=data)


@given("following telemetry data")
def step_impl(context):
    for row in context.table:
        d = dict(
            (x, (datetime_from_str(y) if x == 'timestamp' else y)) for x, y in
            row.as_dict().items())
        x = Telemetry(**d)
        db.session.add(x)
    db.session.commit()
