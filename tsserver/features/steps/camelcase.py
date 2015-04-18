from behave import *
from tsserver.strutils import to_camel_case


@when("I convert {snake_case} to camel case")
def step_impl(context, snake_case):
    context.rv = to_camel_case(snake_case)
