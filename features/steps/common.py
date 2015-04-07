from behave import *


@when("I request {url}")
def step_impl(context, url):
    context.rv = context.request(url)


@then("{code:d} status code should be returned")
def step_impl(context, code):
    assert context.rv.status_code == code


@then('"{key}" key in returned JSON data should contain text "{text}"')
def step_impl(context, key, text):
    assert context.rv.json_data[key] == text
