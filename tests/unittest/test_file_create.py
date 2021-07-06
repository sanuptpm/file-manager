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


@patch("src.main.os.listdir")
@patch('src.main.os.chdir')
def test_get_all_files_exception(mock_chdir, mock_listdir, client):
    mock_listdir.side_effect = Exception()
    res = client.get('/files')
    """res.get_data(), res.status_code, res """
    assert res.status_code == 500


@patch("src.main.f")
@patch('src.main.open')
@patch('src.main.os.chdir')
@patch('src.main.os.makedirs')
@patch('src.main.os.umask')
@patch('src.main.os.path')
def test_create_file(mock_path, mock_umask, mock_dir, mock_chdir, mock_open, mock_write, client):
    res = client.post('/files', json={
        "name": "my4u",
        "data": "New file created"
    })
    data = json.loads(res.get_data(as_text=True))
    """res.get_data(), res.status_code, res """
    assert res.status_code == 409

    res = client.post('/files', json={
        "data": "New file created"
    })
    data = json.loads(res.get_data(as_text=True))
    """res.get_data(), res.status_code, res """
    assert res.status_code == 400

    mock_path.join.return_value = False
    mock_path.exists.return_value = True
    mock_umask.return_value = True
    mock_dir.return_value = False

    mock_path.isfile.return_value = False
    res = client.post('/files', json={
        "name": "my4u",
        "data": "New file created"
    })
    data = json.loads(res.get_data(as_text=True))
    mock_write.writelines.return_value = True
