import json
from unittest.mock import patch

import pytest

from src.main import app as flask_app


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@patch('src.main.os.chdir')
@patch('src.main.os.remove')
def test_delete_file(mock_file, mock_chdir, client):
    mock_file.side_effect = Exception('[Errno 2] No such file or directory: f.txt!')
    res = client.delete('/files/abc')
    """res.get_data(), res.status_code, res """
    assert res.status_code == 404


@patch('src.main.os.chdir')
@patch('src.main.os.remove')
def test_delete_file_success(mock_file, mock_chdir, client):
    mock_file.return_value = {
        "message": "Successfully deleted",
        "name": "m"
    }
    res = client.delete('/files/abc')
    """res.get_data(), res.status_code, res """
    assert res.status_code == 200
