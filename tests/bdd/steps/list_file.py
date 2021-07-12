import requests
from behave import *


@given('searching for file listing')
def step_searching_for_file_listing(context):
    pass


@when('get all matching files')
def step_searching_for_file_listing(context):
    try:
        response = requests.get('http://0.0.0.0:4000/files')
        context.response_body = response.json()
        context.status_code = response.status_code
        context.exception = None
    except Exception as e:
        context.exception = e
    assert context.exception is None


@then('show all file name')
def step_searching_for_file_listing(context):
    assert context.status_code == 200


@when('no matching files found')
def step_searching_for_file_listing(context):
    try:
        response = requests.get('http://0.0.0.0:4000/files')
        context.response_body = response.json()
        context.status_code = response.status_code
        context.exception = None
    except Exception as e:
        context.exception = e
    assert context.exception is None


@then('nothing will show')
def step_searching_for_file_listing(context):
    assert context.status_code == 200
