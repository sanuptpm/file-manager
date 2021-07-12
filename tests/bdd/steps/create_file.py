import requests
from behave import *


@given("get create input {file_name}")
def step_get_create_file(context, file_name):
    context.file_name = file_name


@when('create new file')
def step_create_file_with_name(context):
    response = requests.post('http://0.0.0.0:4000/files', json={
        "data": "New file created",
        "name": context.file_name
    })
    context.response_body = response.json()
    context.status_code = response.status_code


@then('show create status')
def step_show_create_file_status(context):
    assert context.status_code == 200


@then('delete created file')
def step_delete_create_file(context):
    response = requests.delete('http://0.0.0.0:4000/files/' + context.file_name)
    assert response.status_code == 200


@given("already exist create input{file_name}")
def step_create_exist_file(context, file_name):
    context.file_name = file_name
    response = requests.post('http://0.0.0.0:4000/files', json={
        "data": "New file created",
        "name": context.file_name
    })
    assert response.status_code == 200


@when('try to create new file with existing file name')
def step_recreate_exist_file(context):
    response = requests.post('http://0.0.0.0:4000/files', json={
        "data": "New file created",
        "name": context.file_name
    })
    context.status_code = response.status_code
    assert context.status_code == 409


@then('already exist create file status')
def step_show_exist_file_status(context):
    assert context.status_code == 409


@then('delete already created file')
def step_delete_exist_file_create(context):
    response = requests.delete('http://0.0.0.0:4000/files/' + context.file_name)
    assert response.status_code == 200


@given("get file name input for invalid data {file_name}")
def step_get_create_file(context, file_name):
    context.file_name = file_name


@when('try to create new file with invalid data')
def step_create_file_with_name(context):
    response = requests.post('http://0.0.0.0:4000/files', json={
        "data": "New file created",
    })
    context.status_code = response.status_code


@then('get error status')
def step_show_create_file_status(context):
    assert context.status_code == 400
