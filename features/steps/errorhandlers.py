from behave import *

@when("the user requests {url}")
def step_impl(context, url):
    context.rv = context.request(url)


@then("{code:d} error should be returned")
def step_impl(context, code):
    assert context.rv.status_code == code


@then('"{key}" key should contain text "{text}"')
def step_impl(context, key, text):
    assert context.rv.json_data[key] == text
