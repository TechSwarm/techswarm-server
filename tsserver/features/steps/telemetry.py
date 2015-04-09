from behave import *

from tsserver import db, models


example_telemetry_data = {
    'temperature': 23.6,
    'pressure': 1000
}


@when("I POST example telemetry data")
def step_impl(context):
    context.rv = context.request('/telemetry', 'POST',
                                 data=example_telemetry_data)


@then("example telemetry data should be saved to the database")
def step_impl(context):
    assert models.Telemetry.query.count() == 1
    assert models.Telemetry.query.all()[0].as_dict() == example_telemetry_data


@when("I POST example telemetry data without {parameter}")
def step_impl(context, parameter):
    data = example_telemetry_data.copy()
    data.pop(parameter)
    context.rv = context.request('/telemetry', 'POST', data=data)


@given("following telemetry data")
def step_impl(context):
    for row in context.table:
        x = models.Telemetry(**row.as_dict())
        db.session.add(x)
    db.session.commit()
