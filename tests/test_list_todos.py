import pytest

from .utils import get_todos, login, create_client

@pytest.fixture
def client():
    return create_client()

def test_not_logged_in(client):
    response = get_todos(client)

    assert 'Location: http://localhost/login' in str(response.headers)
    assert response.status_code == 302

def test_success(client):
    login(client)
    get_todos_response = get_todos(client)

    assert b'Vivamus tempus' in get_todos_response.data
    assert b'Accumsan nunc vitae' in get_todos_response.data
    # owned by user2
    assert b'Lorem ipsum' not in get_todos_response.data
