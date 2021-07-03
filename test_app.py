import json
import os
from unittest import mock

import pytest
from unittest.mock import patch
from app import app as flask_app


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def test_index(client):
    res = client.get('/')
    assert res.status_code == 200
    expected = {'hello': 'world'}
    assert expected == json.loads(res.get_data(as_text=True))


@patch("app.os.listdir")
@patch('app.os.chdir')
def test_get_files(mock_chdir, mock_listdir, client):
    mock_listdir.return_value = ['file.txt', 'file.doc', 'my4.txt', 'my1.txt', 'my2.txt', '.txt', 'my.txt', 'my3.txt']
    res = client.get('/files')
    print("get_data 1111 >>>>", res.get_data())
    assert res.status_code == 200


@patch('app.os.chdir')
@patch('app.open')
def test_get_file_content(mock_file, mock_chdir, client):
    mock_file.side_effect = Exception('[Errno 2] No such file or directory: f.txt!')
    res = client.get('/files/abc')
    print("get_data 1111 >>>>", res.get_data(), res.status_code)
    assert res.status_code == 404


@patch('app.os.chdir')
@patch('app.os.remove')
def test_delete_file(mock_file, mock_chdir, client):
    mock_file.side_effect = Exception('[Errno 2] No such file or directory: f.txt!')
    res = client.delete('/files/abc')

    print("get_data 1111 >>>>", res.get_data(), res.status_code, res)
    assert res.status_code == 404


@patch('app.os.chdir')
@patch('app.os.rename')
def test_patch_file(mock_file, mock_chdir, client):
    mock_file.side_effect = Exception('[Errno 2] No such file or directory: my.txt -> abc.txt')
    res = client.patch('/files/my', json={'name': 'abc'})
    print("get_data 1111 >>>>", res.get_data(), res.status_code, res)
    assert res.status_code == 404


@patch('app.open')
@patch('app.os.chdir')
@patch('app.os.rename')
def test_update_file(mock_rename, mock_chdir, mock_file, client):
    mock_rename.side_effect = Exception('[Errno 2] No such file or directory: my.txt -> abc.txt')
    res = client.put('/files/my', json={'data': 'updated data'})
    """ res.get_data() res.status_code """
    assert res.status_code == 404


@patch('app.SECRET_KEY')
def test_get_env(mock_key, client):
    mock_key.return_value = 'SECRET_KEY'
    res = client.get('/env')
    print("UUUUUUUUU", res.get_data())