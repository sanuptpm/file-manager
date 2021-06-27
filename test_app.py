import json

import pytest

from app import app as flask_app


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def test_index(app, client):
    res = client.get('/')
    print("gggggggggggg", res, json.loads(res.get_data(as_text=True)))
    assert res.status_code == 200
    expected = {'hello': 'world'}
    assert expected == json.loads(res.get_data(as_text=True))


def test_get_files(app, client):
    res = client.get('/files')
    print("gggggg", res.get_data())
