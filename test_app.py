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
@patch('os.chdir')
def test_get_files(mock_chdir, mock_listdir, client):
    mock_listdir.return_value = ['myfile.txt', 'myfile.doc', 'my4.txt', 'my1.txt', 'my2.txt', '.txt', 'my (copy).txt', 'my3.txt']
    res = client.get('/files')
    print("get_data 1111 >>>>", res.get_data())
    print("get_data >>>>", os.listdir())
    assert res.status_code == 200

