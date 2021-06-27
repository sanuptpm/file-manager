from app import get_port


def test_get_port():
    """
    return port
    """
    assert get_port() == 4000
