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


@patch('src.main.os.chdir')
@patch('src.main.os.rename')
def test_patch_file(mock_file, mock_chdir, client):
    mock_file.side_effect = Exception('[Errno 2] No such file or directory: my.txt -> abc.txt')
    res = client.patch('/files/my', json={'name': 'abc'})
    """res.get_data(), res.status_code, res """
    assert res.status_code == 404


@patch('src.main.os.chdir')
@patch('src.main.os.rename')
def test_patch_file_success(mock_file, mock_chdir, client):
    mock_file.return_value = {
        "message": "successfully updated file name",
        "name": "abc"
    }
    res = client.patch('/files/my', json={'name': 'abc'})
    """res.get_data(), res.status_code, res """
    assert res.status_code == 200


@patch('src.main.os.path')
@patch('src.main.open')
@patch('src.main.os.chdir')
@patch('src.main.os.rename')
def test_update_file(mock_rename, mock_chdir, mock_file, mock_path, client):
    mock_file.side_effect = FileOpenMock(None)
    mock_path.exists.return_value = False
    mock_rename.side_effect = Exception('[Errno 2] No such file or directory: my.txt -> abc.txt')
    res = client.put('/files/my', json={'data': 'updated data'})
    """ res.get_data() res.status_code """
    assert res.status_code == 404

    mock_path.exists.return_value = True
    res = client.put('/files/my', json={'data': 'updated data'})
    """res.get_data(), res.status_code, res """
    assert res.status_code == 200
