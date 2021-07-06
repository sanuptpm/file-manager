import json
from unittest.mock import patch

import pytest

from src.main import app as flask_app
from src.main import get_port, get_secret_key
from src.file import FileOpenMock


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


@patch("src.main.os.listdir")
@patch('src.main.os.chdir')
def test_get_all_files(mock_chdir, mock_listdir, client):
    mock_listdir.return_value = ['file.txt', 'file.doc', 'my4.txt', 'my1.txt', 'my2.txt', '.txt', 'my.txt', 'my3.txt']
    res = client.get('/files')
    """res.get_data(), res.status_code, res """
    assert res.status_code == 200


@patch("src.main.os.listdir")
@patch('src.main.os.chdir')
def test_get_all_files_exception(mock_chdir, mock_listdir, client):
    mock_listdir.side_effect = Exception()
    res = client.get('/files')
    """res.get_data(), res.status_code, res """
    assert res.status_code == 500


@patch('src.main.os.chdir')
@patch('src.main.open')
def test_get_file_content_exception(mock_file, mock_chdir, client):
    mock_file.side_effect = Exception('[Errno 2] No such file or directory: f.txt!')
    res = client.get('/files/abc')
    """res.get_data(), res.status_code, res """
    assert res.status_code == 500


@patch('src.main.os.chdir')
@patch('src.main.fnmatch.filter')
def test_get_all_files(mock_file, mock_chdir, client):
    mock_file.side_effect = Exception('Something went wrong')
    res = client.get('/files')
    """res.get_data(), res.status_code, res """
    assert res.status_code == 500


@patch("src.main.f")
@patch('src.main.open')
@patch('src.main.os.chdir')
def test_get_file_content(mock_chdir, mock_open, mock_read, client):
    mock_read.return_value = 'content of file'
    res = client.get('/files/myu')
    """res.get_data(), res.status_code, res """
    assert res.status_code == 200


@patch('src.main.os.environ.get')
def test_get_port(mock_env):
    mock_env.return_value = 4000
    tmp = get_port()
    assert tmp == 4000
    mock_env.return_value = None
    tmp = get_port()
    assert tmp == 4000


@patch('src.main.os.environ.get')
def test_get_env(mock_key, client):
    mock_key.return_value = 'SECRET_KEY_TEST'
    tmp = get_secret_key()
    res = client.get('/env')
    assert res.status_code == 200
    assert tmp == 'SECRET_KEY_TEST'

    mock_key.return_value = None
    tmp = get_secret_key()
    assert res.status_code == 200
    assert tmp == 'SECRET_KEY'


@patch('src.main.os.environ.get')
def test_get_env_exception(mock_key, client):
    mock_key.side_effect = Exception()
    res = client.get('/env')
    assert res.status_code == 500
