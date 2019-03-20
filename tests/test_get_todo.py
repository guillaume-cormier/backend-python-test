import pytest

from .utils import login, create_client

@pytest.fixture
def client():
    return create_client()

def test_not_logged_in(client):
    response = get_todo(client, 1)

    assert 'Location: http://localhost/login' in str(response.headers)
    assert response.status_code == 302

def test_wrong_user(client):
    login(client, username='user2', password='user2')
    # id 1 belongs to user1
    response = get_todo(client, 1)

    assert response.status_code == 404

def test_success(client):
    login(client)
    get_todo_response = get_todo(client, 1)

    assert b'Vivamus tempus' in get_todo_response.data

def get_todo(client, todo_id):
    path = '/todo/%d' % todo_id
    return client.get(path, follow_redirects=False)
