import requests
from behave import *


@given("get update file name{file_name}")
def step_update_file(context, file_name):
    context.file_name = file_name
    response = requests.post('http://0.0.0.0:4000/files', json={
        "data": "New file created",
        "name": context.file_name
    })
    assert response.status_code == 200


@when('update existing file')
def step_update_file(context):
    response = requests.put('http://0.0.0.0:4000/files/' + context.file_name, json={
        "data": " Description is the pattern  of the four basic modes. "
    })
    context.status_code = response.status_code


@then('show update existing status')
def step_update_status(context):
    assert context.status_code == 200


@then('delete update existing file')
def step_delete_exist_file_create(context):
    response = requests.delete('http://0.0.0.0:4000/files/' + context.file_name)
    assert response.status_code == 200


@given("get update none existing file name {file_name}")
def step_update_file(context, file_name):
    context.file_name = file_name


@when('update none existing file')
def step_update_file(context):
    response = requests.put('http://0.0.0.0:4000/files/' + context.file_name, json={
        "data": " Description is the pattern  of the four basic modes. "
    })
    context.status_code = response.status_code


@then('show update status of none existing')
def step_update_status(context):
    assert context.status_code == 404


