import requests
from behave import *


@given("get delete input {input}")
def step_searching_for_file(context, input):
    response = requests.post('http://0.0.0.0:4000/files', json={
        "data": "New file created",
        "name": input
    })
    context.name = input
    assert response.status_code == 200


@when('create delete file')
def step_delete_file(context):
    response = requests.delete('http://0.0.0.0:4000/files/' + context.name)
    context.response_body = response.json()
    context.status_code = response.status_code


@then('delete file')
def step_show_success(context):
    assert context.status_code == 200


@given("get delete file name {input}")
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
