from behave import *
from flask import json


@when("I request {url:S}")
def step_impl(context, url):
    context.rv = context.request(url)


@then("{code:d} status code should be returned")
def step_impl(context, code):
    assert context.rv.status_code == code


@then('"{key}" key in JSON data should be equal to "{text}"')
def step_impl(context, key, text):
    assert str(context.rv.json_data[key]) == text


@then("following JSON data should be sent")
def step_impl(context):
    # In case of "the same JSON data should be sent" step being used
    # further, save last JSON data here
    context.last_json_data = json.loads(context.text)
    assert context.rv.json_data == context.last_json_data


@then("the same JSON data should be sent")
def step_impl(context):
    assert context.rv.json_data == context.last_json_data


@step('{header} header should be equal to "{value}"')
def step_impl(context, header, value):
    assert context.rv.headers[header] == value
