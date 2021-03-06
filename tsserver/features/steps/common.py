from behave import *
from flask import json


@when("I request {url:S}")
def step_impl(context, url):
    context.rv = context.request(url)


@when("I request {url:S} via {method}")
def step_impl(context, url, method):
    context.rv = context.request(url, method)


@when("I {method} following data to {url}")
def step_impl(context, method, url):
    context.rv = context.request(url, method, data=context.table[0].as_dict())


@then("{code:d} status code should be returned")
def step_impl(context, code):
    assert context.rv.status_code == code, context.rv.status_code


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


@then("{value} should be returned")
def step_impl(context, value):
    assert context.rv == value


@given("I am authenticated")
def step_impl(context):
    context.authenticate()
