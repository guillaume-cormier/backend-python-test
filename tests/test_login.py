import pytest

from .utils import login, create_client

@pytest.fixture
def client():
    return create_client()

def test_invalid_username(client):
    response = login(client, username='invalid')

    assert 'Location: http://localhost/login' in str(response.headers)
    assert response.status_code == 302

def test_invalid_password(client):
    response = login(client, username='user1', password='invalid')

    assert 'Location: http://localhost/login' in str(response.headers)
    assert response.status_code == 302

def test_success(client):
    response = login(client)

    assert 'Location: http://localhost/todo' in str(response.headers)
    assert response.status_code == 302
