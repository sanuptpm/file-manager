import json
from unittest.mock import patch

import pytest

from application import app as flask_app
from application.app import get_port, get_secret_key
from application.file import FileOpenMock


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
def test_get_all_files(mock_chdir, mock_listdir, client):
    mock_listdir.return_value = ['file.txt', 'file.doc', 'my4.txt', 'my1.txt', 'my2.txt', '.txt', 'my.txt', 'my3.txt']
    res = client.get('/files')
    """res.get_data(), res.status_code, res """
    assert res.status_code == 200


@patch("app.os.listdir")
@patch('app.os.chdir')
def test_get_all_files_exception(mock_chdir, mock_listdir, client):
    mock_listdir.side_effect = Exception()
    res = client.get('/files')
    """res.get_data(), res.status_code, res """
    assert res.status_code == 500


@patch('app.os.chdir')
@patch('app.open')
def test_get_file_content(mock_file, mock_chdir, client):
    mock_file.side_effect = Exception('[Errno 2] No such file or directory: f.txt!')
    res = client.get('/files/abc')
    """res.get_data(), res.status_code, res """
    assert res.status_code == 404


@patch('app.os.chdir')
@patch('app.os.remove')
def test_delete_file(mock_file, mock_chdir, client):
    mock_file.side_effect = Exception('[Errno 2] No such file or directory: f.txt!')
    res = client.delete('/files/abc')
    """res.get_data(), res.status_code, res """
    assert res.status_code == 404


@patch('app.os.chdir')
@patch('app.os.remove')
def test_delete_file_success(mock_file, mock_chdir, client):
    mock_file.return_value = {
        "message": "Successfully deleted",
        "name": "m"
    }
    res = client.delete('/files/abc')
    """res.get_data(), res.status_code, res """
    assert res.status_code == 200


@patch('app.os.chdir')
@patch('app.os.rename')
def test_patch_file(mock_file, mock_chdir, client):
    mock_file.side_effect = Exception('[Errno 2] No such file or directory: my.txt -> abc.txt')
    res = client.patch('/files/my', json={'name': 'abc'})
    """res.get_data(), res.status_code, res """
    assert res.status_code == 404


@patch('app.os.chdir')
@patch('app.os.rename')
def test_patch_file_success(mock_file, mock_chdir, client):
    mock_file.return_value = {
        "message": "successfully updated file name",
        "name": "abc"
    }
    res = client.patch('/files/my', json={'name': 'abc'})
    """res.get_data(), res.status_code, res """
    assert res.status_code == 200


@patch('app.os.path')
@patch('app.open')
@patch('app.os.chdir')
@patch('app.os.rename')
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


@patch('app.os.chdir')
@patch('app.fnmatch.filter')
def test_get_all_files(mock_file, mock_chdir, client):
    mock_file.side_effect = Exception('Something went wrong')
    res = client.get('/files')
    """res.get_data(), res.status_code, res """
    assert res.status_code == 500


@patch("app.f")
@patch('app.open')
@patch('app.os.chdir')
def test_get_file_content(mock_chdir, mock_open, mock_read, client):
    mock_read.return_value = 'content of file'
    res = client.get('/files/myu')
    """res.get_data(), res.status_code, res """
    assert res.status_code == 200


@patch('app.os.environ.get')
def test_get_port(mock_env):
    mock_env.return_value = 4000
    tmp = get_port()
    assert tmp == 4000
    mock_env.return_value = None
    tmp = get_port()
    assert tmp == 4000


@patch('app.os.environ.get')
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


@patch('app.os.environ.get')
def test_get_env_exception(mock_key, client):
    mock_key.side_effect = Exception()
    res = client.get('/env')
    assert res.status_code == 500


@patch("app.f")
@patch('app.open')
@patch('app.os.chdir')
@patch('app.os.makedirs')
@patch('app.os.umask')
@patch('app.os.path')
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
