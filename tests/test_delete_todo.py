import pytest

from .utils import get_todo_json, get_todos, login, create_client

@pytest.fixture
def client():
    return create_client()

def test_not_logged_in(client):
    response = delete_todo(client, 1)

    assert 'Location: http://localhost/login' in str(response.headers)
    assert response.status_code == 302

def test_wrong_user(client):
    login(client, username='user2', password='user2')
    # id 1 belongs to user1
    response = delete_todo(client, 1)

    assert response.status_code == 404

def test_success(client):
    login(client)
    delete_response = delete_todo(client, 1)
    get_todo_response = get_todo_json(client, 1)
    get_todos_response = get_todos(client)

    assert 'Location: http://localhost/todo' in str(delete_response.headers)
    assert delete_response.status_code == 302
    assert get_todo_response.status_code == 404
    assert b'Item deleted.' in get_todos_response.data

def delete_todo(client, todo_id):
    path = '/todo/%d' % todo_id
    return client.post(path, follow_redirects=False)
