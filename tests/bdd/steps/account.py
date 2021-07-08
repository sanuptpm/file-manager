
from behave import *


@given('a sample text loaded into the frobulator')
def step_given_put_thing_into_blender(context):
    print("dddddddddddddd", context.text)
    pass


@when('we activate the frobulator')
def step_when_switch_blender_on(context):
    print("dddddddddddddd", context.text)
    assert True is not False


@then('we will find it similar to English')
def step_then_should_transform_into(context):
    print("dddddddddddddd", context.text)
    assert context.failed is False
