import requests
from behave import *


@given("get file name for delete {input}")
def step_searching_for_file(context, input):
    context.name = input


@given("create new file for delete")
def step_searching_for_file(context):
    response = requests.post('http://0.0.0.0:4000/files', json={
        "data": "New file created",
        "name": context.name
    })


@when('delete existing file')
def step_delete_file(context):
    response = requests.delete('http://0.0.0.0:4000/files/' + context.name)
    context.response_body = response.json()
    context.status_code = response.status_code


@then('show delete file status')
def step_show_success(context):
    assert context.status_code == 200


@given("get data for delete file {input}")
def step_searching_for_file(context, input):
    context.name = input


@when('no matching files found for delete')
def step_delete_file(context):
    response = requests.delete('http://0.0.0.0:4000/files/' + context.name)
    context.response_body = response.json()
    context.status_code = response.status_code


@then('show file not found status for delete')
def step_show_success(context):
    assert context.status_code == 404
